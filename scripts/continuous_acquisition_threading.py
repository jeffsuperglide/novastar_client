"""Continuous data extraction from the NovaStar API"""

import logging
import logging.handlers
import os
import platform
import random
import re
import sys
import tomllib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Union

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

logger = logging.getLogger("extract")


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


def _load_toml_config(path: Union[str, Path]) -> dict[str, Any]:
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

    for station_id, station_data in cfg["station"].items():
        network = station_data["network"]
        for ts in station_data["series"]:
            if not ts.get("enabled", False):
                continue

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
        dssfile,
    ) = task

    try:
        logger.info("Get timeseries data for '%s'.", ns_tsid)
        ns_client = NovaStarClient(ns_config)

        response = ns_client.timeseries.get(
            tsid=ns_tsid,
            periodStart=period_start,
            periodEnd=period_end,
        )

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

        if shef_lookup_parameter == "" or len(shef_lookup_parameter) <= 0:
            raise ValueError(f"No parameter found for TSID '{ns_tsid}'.")

        timeseries = response.timeseries
        if timeseries.units == "pies":
            logger.info("Time series units 'pies' found and converting to 'ft'.")
            timeseries.units = "ft"

        dss_interval = DssTimeInterval.validate_time_string(interval)
        logger.info(
            "NovaStar interval '%s' converted to DSS interval '%s'.",
            interval,
            dss_interval,
        )

        path = (
            f"/{station_id_tag}/{timeseries_properties.station_name}/"
            f"{shef_lookup_parameter}//{dss_interval}/{timeseries.data_type}/"
        )
        logger.info("TSID: '%s'; DSS: '%s'", ns_tsid, path)

        dt_value = response.get_data_fields("dt", "value")
        fraction = 0.75
        n = max(1, int(len(dt_value) * fraction))
        subset = random.sample(dt_value, n)
        logger.debug(
            "Random sample of time/value (%d of %d): %s", n, len(dt_value), subset
        )

        rows_written = 0
        if len(dt_value) > 0:
            df = pd.DataFrame(dt_value)
            df["dt"] = pd.to_datetime(df["dt"])
            df["dt"] = df["dt"].dt.tz_convert("UTC")

            tsc = RegularTimeSeries()
            tsc.id = path
            tsc.values = df["value"].to_list()  # type: ignore
            tsc.times = df["dt"].to_list()
            tsc.units = timeseries.units  # type: ignore
            tsc.data_type = ns5_type_to_dss(statistic)

            with HecDss(dssfile) as dss:
                dss.put(tsc)

            rows_written = len(dt_value)
            logger.info("Put %d values into DSS path %s.", rows_written, path)

        return {
            "ns_tsid": ns_tsid,
            "path": path,
            "rows_written": rows_written,
            "ok": True,
            "error": None,
        }

    except Exception as exc:
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

    config_path = Path(sys.argv[1])

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
