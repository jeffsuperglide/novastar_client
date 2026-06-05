# Simple Notes

## Running the ***continuous_acquisition*** script

- This script does require a TOML configuration file.
- Set `logger` settings in the TOML config.
- Define a logger file in the TOML config for logging information.
- DSS log output will not save to the file.
- Remove or comment out the logger.file for no log file.
- Define the DSS file.
- Define the period.start and period.end for all time series.
- Target specific time series by setting the `enabled` boolean.

## Running on Windows and reducing command line output

### PowerShell

- python script.py config.toml > $nul   # discard stdout
- python script.py config.toml *> $nul  # discard all streams

### Command Prompt

- python script.py config.toml > NUL        rem discard stdout
- python script.py config.toml > NUL 2>&1   rem discard stdout and stderr

### Linux

- python script.py config.toml > /dev/null
