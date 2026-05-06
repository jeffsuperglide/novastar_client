# Jython Example Script

```jython
# name=ns5acpTS
# displayinmenu=false
# displaytouser=false
# displayinselector=false
from hec.script import Plot
from hec.io import TimeSeriesContainer
#from hec.io import PairedDataContainer
#from hec.hecmath import TimeSeriesMath
#from hec.hecmath import PairedDataMath
from hec.heclib.dss import HecDss, DSSPathname
from hec.heclib.util import HecTime
from hec.script import MessageBox
#import java

#!/usr/bin/env jython

import subprocess
import json
import sys

# Set this path pointing to your ns5acp CLI if not available on the command line.
# This is usually the case if you are using a virtual environment.
# Check if the CLI is installed by running 'ns5acp --version'.
# If you get a response 'ns5acp, version...' and not in virtual environment,
# replace 'NS5ACP' in the cmd = [] with "ns5acp".
NS5ACP = "C:\\path\\to\\cli\\ns5acp.exe"


def run_ns5acp_ts_once():
    cmd = [
        NS5ACP,
        "ts",
        "--tsid", "54-5400.NovaStar5.WaterLevelRiver-Mean.15Minute",
        "--period-start", "now_minus_1Day",
        "--period-end", "now"
    ]

    try:
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout_data, stderr_data = p.communicate()
        rc = p.returncode

        if rc != 0:
            sys.stderr.write("ns5acp failed with return code %d\n" % rc)
            if stderr_data:
                sys.stderr.write(stderr_data)
            return

        if not stdout_data:
            print("No output received from ns5acp.")
            return


        records = json.loads(stdout_data)
        times = []
        values = []
        for rec in records:
            dt = rec.get("dt")
            value = rec.get("value")
            dt_value = HecTime(dt).value()
            times.append(dt_value)
            values.append(value)
#            print(dt_value, value)
        try:
            myDss = HecDss.open("myFile.dss")
            tsc = TimeSeriesContainer()
            tsc.fullName = "/54-5400/Gatun Lake/Stage//15Minute/WaterLevelRiver-Mean/"
            tsc.interval = 60
            tsc.times = times
            tsc.values = values
            tsc.numberValues = len(values)
            tsc.units ="FT"
            tsc.type = "PER-AVER"
            myDss.put(tsc)
        except Exception, e:
           print(''.join(e.args),"Python Error")
        
        finally:
            myDss.close()

    except OSError, e:
        sys.stderr.write("Error executing ns5acp: %s\n" % str(e))


def run_ns5acp_ts_stream():
    cmd = [
        NS5ACP,
        "ts",
        "--tsid", "54-5400.NovaStar5.WaterLevelRiver-Mean.15Minute",
        "--period-start", "now_minus_2Days",
        "--period-end", "now",
        "--stream"
    ]

    try:
        # bufsize=1 requests line buffering; stdout is a pipe
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1
        )

        # Read stdout line by line until the process ends.
        times = []
        values = []
        while True:
            line = p.stdout.readline()
            if not line:
                break  # EOF

            line = line.strip()
            if not line:
                continue

            try:
                rec = json.loads(line)
            except Exception, e:
                sys.stderr.write("Failed to parse JSON line: %s\n" % str(e))
                sys.stderr.write("Raw line was:\n%s\n" % line)
                continue

            dt = rec.get("dt")
            value = rec.get("value")
            times.append(HecTime(dt).value())
            values.append(value)

        # Make sure process has finished, get stderr and return code
        stderr_data = p.stderr.read()
        rc = p.wait()

        if rc != 0:
            sys.stderr.write("ns5acp --stream failed with return code %d\n" % rc)
            if stderr_data:
                sys.stderr.write(stderr_data)

        try:
            myDss = HecDss.open("myFile.dss")
            tsc = TimeSeriesContainer()
            tsc.fullName = "/54-5400/Gatun Lake/Stage//15Minute/WaterLevelRiver-Mean/"
            tsc.interval = 60
            tsc.times = times
            tsc.values = values
            tsc.numberValues = len(values)
            tsc.units ="FT"
            tsc.type = "PER-AVER"
            myDss.put(tsc)
        except Exception, e:
           print(''.join(e.args),"Python Error")
        
        finally:
            myDss.close()


    except OSError, e:
        sys.stderr.write("Error executing ns5acp with --stream: %s\n" % str(e))


if __name__ == "__main__":
    # Choose which behavior you want
#    run_ns5acp_ts_once()
    run_ns5acp_ts_stream()
```
