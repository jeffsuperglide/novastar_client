"""Continuous data extraction from the NovaStar API"""

import logging
import logging.handlers
import os
import platform
import re
import sys
import tomllib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import pandas as pd
from hecdss.hecdss import HecDss, RegularTimeSeries

from novastar_client.client import NovaStarClient
from novastar_client.config import NovaStarConfig
from novastar_client.logging_utils import configure_package_logging
from novastar_client.transform.dss_data_type import ns5_type_to_dss
from novastar_client.transform.dss_time_interval import DssTimeInterval
from novastar_client.transform.shef_lookup import get_shef_info

MAX_THREADING = 4
DEFAULT_MAX_BYTES = 500_000
DEFAULT_LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"

logger = logging.getLogger("extract")

_SIZE_RE = re.compile(
    r"^\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>b|kb|k|mb|m|gb|g)?\s*$",
    re.IGNORECASE,
)

_SIZE_UNITS = {
    None: 1,
    "b": 1,
    "k": 1024,
    "kb": 1024,
    "m": 1024**2,
    "mb": 1024**2,
}


def _exit_with_warning(msg: str, exc: Exception | None = None) -> None:
    logger.warning(msg)
    if exc is None:
        raise SystemExit(1)
    raise SystemExit(1) from exc


def _parse_max_bytes(value):
    if isinstance(value, int):
        return value

    s = value.strip()
    if not s:
        logger.info("maxBytes cannot be empty.")
        return DEFAULT_MAX_BYTES

    if s.isdigit():
        return int(s)

    match = _SIZE_RE.match(s)
    if not match:
        logger.info(
            "Invalid maxBytes value: %r. Use an integer or a size like 1KB, 10MB. "
            "Returning default max bytes %d",
            value,
            DEFAULT_MAX_BYTES,
        )
        return DEFAULT_MAX_BYTES

    number = float(match.group("value"))
    unit = match.group("unit")
    multiplier = _SIZE_UNITS[unit.lower() if unit else None]
    size = int(number * multiplier)

    if size < 0:
        logger.info("maxBytes must be >= 0")
        return DEFAULT_MAX_BYTES

    return size


def _configure_logger(cfg: dict) -> None:
    if not isinstance(cfg, dict):
        logger.warning("Invalid logger config; expected a table.")
        return

    level = cfg.get("level")
    if level is not None:
        try:
            logger.setLevel(str(level).upper())
        except ValueError:
            logger.warning(
                "Invalid logger level in config (%r); keeping existing level",
                level,
            )

    fmt = cfg.get("format")
    try:
        formatter = logging.Formatter(fmt)
    except ValueError:
        logger.warning(
            "Invalid logger format in config (%r); using default format",
            fmt,
        )
        formatter = logging.Formatter(DEFAULT_LOG_FORMAT)

    log_file = cfg.get("file")
    if log_file is not None:
        max_bytes = cfg.get("max_bytes", DEFAULT_MAX_BYTES)
        max_bytes_parsed = _parse_max_bytes(max_bytes)
        backup_count = cfg.get("backup_count", 1)
        try:
            log_path = Path(log_file).expanduser().absolute()
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.handlers.RotatingFileHandler(
                log_path,
                mode="a",
                maxBytes=max_bytes_parsed,
                backupCount=backup_count,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except (OSError, ValueError):
            logger.warning(
                "Invalid logger file in config (%r); file logging not enabled",
                log_file,
            )


def _dss_file_path(cfg: dict) -> Path:
    default_dssfile = Path("timeseries.dss")
    dss_cfg = cfg.get("dss", {})
    if not isinstance(dss_cfg, dict):
        logger.warning("Invalid dss config; expected a table.")
        return default_dssfile

    dssfile = dss_cfg.get("file")
    if dssfile is not None:
        return Path(dssfile).expanduser().absolute()

    return default_dssfile


def _load_toml_config(path: str | Path) -> dict[str, Any]:
    path = Path(path)

    try:
        with path.open("rb") as f:
            config = tomllib.load(f)
    except FileNotFoundError as exc:
        _exit_with_warning(f"Config file not found: {path}", exc)
    except PermissionError as exc:
        _exit_with_warning(f"No permission to read config file: {path}", exc)
    except tomllib.TOMLDecodeError as exc:
        _exit_with_warning(f"Invalid TOML in config file {path}: {exc}", exc)

    return config


def _apply_fill_config(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    out = df.copy()

    for method_name in config.get("order", []):
        opts = dict(config.get(method_name, {}))
        if not opts.pop("enabled", False):
            continue

        if method_name == "ffill":
            out = out.ffill(**opts)

        elif method_name == "interpolate":
            out = out.interpolate(**opts)

        elif method_name == "fillna":
            out = out.fillna(**opts)

        else:
            raise ValueError(f"Unknown fill method in config: {method_name}")

    return out


def _safe_tz_convert(df: pd.DataFrame, col: str, timezone: str | None) -> pd.DataFrame:
    if timezone is None:
        return df

    try:
        tz = ZoneInfo(timezone)
        series = df[col]

        if not pd.api.types.is_datetime64_any_dtype(series):
            series = pd.to_datetime(series, errors="raise")

        if series.dt.tz is None:
            raise ValueError(f"column {col!r} is timezone-naive, cannot tz_convert")

        df[col] = series.dt.tz_convert(tz)

    except (ZoneInfoNotFoundError, ValueError, TypeError, KeyError) as e:
        logger.warning(
            f"tz_convert skipped for column {col!r} with timezone {timezone!r}: {e}"
        )
        # df[col] left unchanged

    return df


def build_tasks(
    cfg: dict[str, Any], ns_config: NovaStarConfig, dssfile: Path
) -> list[tuple]:
    tasks = []

    cfg_period = cfg["period"]
    period_start = cfg_period.get("start")
    period_end = cfg_period.get("end")
    logger.info(
        "NovaStar Client Timewindow: start '%s', end '%s'", period_start, period_end
    )

    # The global parameters
    global_parameters = cfg.get("timeseries_parameters", {})
    global_fill_options = cfg.get("fill", {})

    for station_id, station_data in cfg["station"].items():
        network = station_data["network"]
        station_parameters = station_data.get("timeseries_parameters", {})
        for ts in station_data["series"]:
            if not ts.get("enabled", False):
                continue

            # series parameters resolved down from global
            series_parameters = ts.get("timeseries_parameters", {})
            resolved_parameters = {
                **global_parameters,
                **station_parameters,
                **series_parameters,
            }

            station_tag = ts.get("tag")
            station_id_tag = (
                f"{station_id}-{station_tag}" if len(station_tag) > 0 else station_id
            )

            parameter = ts.get("parameter")
            statistic = ts.get("statistic")
            parameter_statistic = (
                f"{parameter}-{statistic}" if len(statistic) > 0 else parameter
            )

            interval = ts.get("interval")
            ns_tsid = f"{station_id_tag}.{network}.{parameter_statistic}.{interval}"
            logger.info("NovaStar time series ID: %s", ns_tsid)

            tasks.append(
                (
                    ns_tsid,
                    period_start,
                    period_end,
                    parameter,
                    statistic,
                    interval,
                    station_id_tag,
                    ns_config,
                    resolved_parameters,
                    global_fill_options,
                    dssfile.as_posix(),
                )
            )

    return tasks


def process_timeseries(task: tuple) -> dict[str, Any]:
    (
        ns_tsid,
        period_start,
        period_end,
        parameter,
        statistic,
        interval,
        station_id_tag,
        ns_config,
        resolved_parameters,
        global_fill_options,
        dssfile,
    ) = task

    try:
        logger.info("Get timeseries data for '%s'.", ns_tsid)
        ns_client = NovaStarClient(ns_config)

        # Using the 'includeMissing' argument creates a regular interval time series,
        # which is needed for DSS put (RegularTimeSeries).
        ts_get_arguments = {
            "tsid": ns_tsid,
            "periodStart": period_start,
            "periodEnd": period_end,
            **resolved_parameters,
        }
        response = ns_client.timeseries.get(**ts_get_arguments)

        if response is None:
            raise ValueError(
                f"Client response for time series '{ns_tsid}' returned None."
            )

        timeseries_properties = response.get_properties()
        logger.debug("TimeSeriesProperties: %s", response.get_properties_asdict())

        ts_properties_shef_code = timeseries_properties.point_type_shef_parameter_code
        shef_lookup_info = get_shef_info(ts_properties_shef_code)
        shef_lookup_parameter = shef_lookup_info.parameter

        logger.info(
            "Parameter lookup from SHEF '%s' translates to '%s'; first try.",
            ts_properties_shef_code,
            shef_lookup_parameter,
        )

        if shef_lookup_parameter == "" or len(shef_lookup_parameter) <= 0:
            datatype = ns_client.datatypes.get(name=parameter)
            if datatype is not None:
                shef_code = datatype.datatypes[0].shef_physical_element
                shef_lookup_info = get_shef_info(shef_code)
                shef_lookup_parameter = shef_lookup_info.parameter
                logger.info(
                    "Parameter lookup from SHEF '%s' translates to '%s'; second try.",
                    shef_code,
                    shef_lookup_parameter,
                )
            # if shef_lookup_parameter == "" or len(shef_lookup_parameter) <= 0:
            raise ValueError(f"No parameter found for TSID '{ns_tsid}'.")

        # Getting the timeseries data from the response.
        timeseries = response.timeseries

        # Change unit name if pies.
        timeseries.units = "ft" if timeseries.units == "pies" else timeseries.units
        logger.info("Time series units 'pies' found and converting to 'ft'.")

        dt_value = response.get_data_fields("dt", "value")

        rows_written = 0
        if len(dt_value) > 0:
            # create the data frame, convert datetimes, and remove seconds and microseconds.
            df = pd.DataFrame(dt_value)

            df["dt"] = pd.to_datetime(df["dt"])
            df.sort_values("dt", inplace=True)

            timezone = resolved_parameters.get("timezone", None)
            df = _safe_tz_convert(df, "dt", timezone)

            df.set_index("dt", inplace=True)

            # Apply fill configurations
            df = _apply_fill_config(df, global_fill_options)

            # Build the DSS pathname.
            dss_interval = DssTimeInterval.validate_time_string(interval)
            dsspath = (
                f"/{station_id_tag}/{timeseries_properties.station_name}/"
                f"{shef_lookup_parameter}//{dss_interval}/{timeseries.data_type}/"
            )
            logger.info("TSID: '%s'; DSS: '%s'", ns_tsid, dsspath)

            # Put the data into DSS
            with HecDss(dssfile) as dss:
                tsc = RegularTimeSeries.create(
                    values=df["value"].to_list(),
                    times=df.index.to_list(),
                    units=timeseries.units,
                    data_type=ns5_type_to_dss(statistic),
                    time_zone_name=timezone if timezone else "EST",
                    path=dsspath,
                )
                dss.put(tsc)

            rows_written = len(dt_value)
            logger.info("Put %d values into DSS path %s.", rows_written, dsspath)

        return {
            "ns_tsid": ns_tsid,
            "path": dsspath,
            "rows_written": rows_written,
            "ok": True,
            "error": None,
        }

    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed processing '%s': %s", ns_tsid, exc)
        return {
            "ns_tsid": ns_tsid,
            "path": None,
            "rows_written": 0,
            "ok": False,
            "error": str(exc),
        }


def main():
    if len(sys.argv) < 2:
        msg = (
            f"{'*~' * 40}"
            f"\nMissing required configuration file.\n\n"
            f"Usage: python {os.path.basename(sys.argv[0])} /path/to/config.toml\n"
            f"{'*~' * 40}"
        )
        _exit_with_warning(msg)

    config_path = Path(sys.argv[1]).expanduser().absolute()

    # load the configurations
    cfg = _load_toml_config(config_path)

    # get the logger setup from toml config
    log_cfg = cfg.get("logger", {})
    _configure_logger(log_cfg)

    # setup NovaStar client and configurations
    client_timeout = cfg.get("client", {}).get("timeout", 30)
    log_formatting = cfg.get("logger", {}).get("format", None)
    level_num = logger.getEffectiveLevel()
    level_name = logging.getLevelName(level_num)

    # startup logging
    logger.setLevel("INFO")
    logger.info("=== Starting script ===")
    logger.info("Python version: %s", platform.python_version())
    logger.info("Working directory: %s", Path.cwd())
    logger.info("Loaded config from '%s'", config_path)
    logger.setLevel(level_name)

    ns_config = NovaStarConfig(
        timeout=client_timeout,
        log_level=level_name,
        log_format=(log_formatting if log_formatting else DEFAULT_LOG_FORMAT),
    )

    configure_package_logging(ns_config)

    dssfile = _dss_file_path(cfg)
    logger.info("DSS file open at '%s'", dssfile)

    tasks = build_tasks(cfg, ns_config, dssfile)
    logger.info("Prepared %d tasks for execution.", len(tasks))

    results = []
    with ThreadPoolExecutor(
        max_workers=min(MAX_THREADING, max(1, len(tasks)))
    ) as executor:
        futures = {executor.submit(process_timeseries, task): task for task in tasks}

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    ok_count = sum(1 for r in results if r["ok"])
    fail_count = len(results) - ok_count
    total_rows = sum(r["rows_written"] for r in results)

    logger.info(
        "Finished processing %d tasks: %d succeeded, %d failed, %d total rows written.",
        len(results),
        ok_count,
        fail_count,
        total_rows,
    )


if __name__ == "__main__":
    main()
