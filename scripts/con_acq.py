"""Continuous data extraction from the NovaStar API"""

import logging.handlers
import os
import random
import re
import sys
import tomllib
from pathlib import Path
import logging
from typing import Union

import pandas as pd

from hecdss.hecdss import HecDss, RegularTimeSeries
from novastar_client.config import NovaStarConfig
from novastar_client.client import NovaStarClient
from novastar_client.logging_utils import configure_package_logging

from novastar_client.transform.dss_data_type import ns5_type_to_dss
from novastar_client.transform.dss_time_interval import DssTimeInterval
from novastar_client.transform.shef_lookup import get_shef_info

logger = logging.getLogger("extract")

DEFAULT_MAX_BYTES = 500_000


def _exit_with_warning(msg: str, exc: Exception | None = None) -> None:
    logger.warning(msg)
    if exc is None:
        raise SystemExit(1)
    raise SystemExit(1) from exc


def _parse_max_bytes(value):
    """
    Parse maxBytes from an int or a human-readable string.

    Accepted examples:
      1048576
      "1048576"
      "1M", "1m", "1MB", "1mb"
      "1K", "1k", "1KB", "1kb"
      "1.5M"

    Returns:
      int: size in bytes

    Raises:
      TypeError: unsupported type
      ValueError: invalid or negative size
    """
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
        # "g": 1024**3,
        # "gb": 1024**3,
    }

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
            "Invalid maxBytes value: %r.  "
            "Use an integer or a size like 1KB, 10MB, 1.5G.  "
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
    # get the logger table.
    log_cfg = cfg.get("logger", {})
    if not isinstance(log_cfg, dict):
        logger.warning("Invalid logger config; expected a table.")
        return

    # get the defined log level.
    level = log_cfg.get("level")
    if level is not None:
        try:
            logger.setLevel(str(level).upper())
        except ValueError:
            logger.warning(
                "Invalid logger level in config (%r); keeping existing level",
                level,
                # exc_info=exc,
            )

    # set the logger format and fall back to default if not there.
    fmt = log_cfg.get("format")
    try:
        formatter = logging.Formatter(fmt)
    except ValueError:
        logger.warning(
            "Invalid logger format in config (%r); using default format",
            fmt,
            # exc_info=exc,
        )
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    # console formatter
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Optional file handler
    log_file = log_cfg.get("file")
    if log_file is not None:
        max_bytes = log_cfg.get("max_bytes", 500_000)
        max_bytes_parsed = _parse_max_bytes(max_bytes)
        backup_count = log_cfg.get("backup_count", 1)
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
                # exc_info=exc,
            )


def _dss_file_path(cfg: dict) -> Path:
    default_dssfile = Path("timeseries.dss")

    # get the dss table.
    log_cfg = cfg.get("dss", {})
    if not isinstance(log_cfg, dict):
        logger.warning("Invalid dss config; expected a table.")
        return default_dssfile

    # get the defined dsss file.
    dssfile = log_cfg.get("file")
    if dssfile is not None:
        dss_file_path = Path(dssfile)
        return dss_file_path.expanduser().absolute()

    return default_dssfile


def _load_toml_config(path: Union[str, Path]) -> dict:
    """load_toml_config"""
    path = Path(path)

    try:
        with path.open("rb") as f:  # use Path.open
            config = tomllib.load(f)
    except FileNotFoundError as exc:
        msg = f"Config file not found: {path}"
        _exit_with_warning(msg, exc)
    except PermissionError as exc:
        msg = f"No permission to read config file: {path}"
        _exit_with_warning(msg, exc)
    except tomllib.TOMLDecodeError as exc:
        msg = f"Invalid TOML in config file {path}: {exc}"
        _exit_with_warning(msg, exc)

    return config


def main():
    """main"""
    # check the first argument and get that argument
    # the first argument should be the toml config
    if len(sys.argv) < 2:
        msg = (
            f"Missing required configuration file.\n\n"
            f"Usage: python {os.path.basename(sys.argv[0])} /path/to/config.toml"
        )
        _exit_with_warning(msg)

    config_path = Path(sys.argv[1])

    # load the configurations
    cfg = _load_toml_config(config_path)

    # get the logger setup from toml config
    _configure_logger(cfg)

    # setup NovaStar client and configurations
    client_timeout = cfg.get("client", {}).get("timeout", 30)
    level_num = logger.getEffectiveLevel()
    level_name = logging.getLevelName(level_num)
    ns_config = NovaStarConfig(timeout=client_timeout, log_level=level_name)
    ns_client = NovaStarClient(ns_config)
    configure_package_logging(ns_config)

    # open the DSS file to write to
    dssfile = _dss_file_path(cfg)
    dss = HecDss(dssfile.as_posix())

    # NovaStar beginning and ending times
    cfg_period = cfg["period"]
    period_start = cfg_period.get("start")
    period_end = cfg_period.get("end")
    logger.info(
        "NovaStar Client Timewindow: start '%s', end '%s'", period_start, period_end
    )

    # loop through the stations from the toml config
    # building the time series id from the configurations
    for station_id, station_data in cfg["station"].items():
        network = station_data["network"]
        for ts in station_data["series"]:
            # check that it is enabled first
            is_enabled = ts.get("enabled", False)
            if not is_enabled:
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

            # get the time series using the toml config tsid build and time window
            response = ns_client.timeseries.get(
                tsid=ns_tsid,
                periodStart=period_start,
                periodEnd=period_end,
            )
            # continue to the next time series if the response is None
            if response is None:
                logger.warning(
                    "Client response for time series '%s' returned None; "
                    "time series will be skipped.",
                    ns_tsid,
                )
                continue

            # getting the shef paramter from NWSLI
            timeseries_properties = response.get_properties()
            logger.debug(
                "TimeSeriesProperties: %s",
                response.get_properties_asdict(),
            )

            # parameter lookup from shef code; first try
            ts_properties_shef_code = (
                timeseries_properties.point_type_shef_parameter_code
            )
            shef_lookup_info = get_shef_info(ts_properties_shef_code)
            shef_lookup_parameter = shef_lookup_info.parameter
            logger.info(
                "Parameter lookup from SHEF '%s' translates to '%s'; first try.",
                ts_properties_shef_code,
                shef_lookup_parameter,
            )

            # Check the shef parameter and try another method if string is empty.
            # Get it from the NovaStar name.
            # Ultimately, not parameter from shef we have to continue.
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

            # parameter lookup from shef code; second try
            if shef_lookup_parameter == "" or len(shef_lookup_parameter) <= 0:
                logger.warning("No parameter found for TSID '%s'.", ns_tsid)
                continue

            # check the units
            timeseries = response.timeseries
            if timeseries.units == "pies":
                logger.info("Time series units 'pies' found and converting to 'ft'.")
                timeseries.units = "ft"

            # getting dss parts
            dss_interval = DssTimeInterval.validate_time_string(interval)
            logger.info(
                "NovaStar interval '%s' converted to DSS interval '%s'.",
                interval,
                dss_interval,
            )

            # Build the DSS path.
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

            if len(dt_value) > 0:
                # load the DataFrame
                df = pd.DataFrame(dt_value)
                # convert dt to datetime
                df["dt"] = pd.to_datetime(df["dt"])
                # convert datetime to UTC
                df["dt"] = df["dt"].dt.tz_convert("UTC")

                tsc = RegularTimeSeries()
                tsc.id = path
                tsc.values = df["value"].to_list()  # type: ignore
                tsc.times = df["dt"].to_list()
                tsc.units = timeseries.units  # type: ignore
                tsc.data_type = ns5_type_to_dss(statistic)

                dss.put(tsc)

    dss.close()


if __name__ == "__main__":
    main()
