""" _summary_
"""

import urllib
import urllib2
import json

from hec.script import MessageBox
from hec.heclib.dss import HecDss, HecTimeSeries
from hec.io import TimeSeriesContainer
from hec.heclib.util import HecTime

def fetch_data(url):
    headers = {"accept":"application/json"}

    req = urllib2.Request(url, headers=headers)

    # fp = urllib2.urlopen(req, timeout=10)
    fp = urllib2.urlopen(req)

    if fp.getcode() == 200:
        try:
            raw = fp.read()
        finally:
            fp.close()

        if isinstance(raw, unicode):
            text = raw
        else:
            text = raw.decode("utf-8")

        return json.loads(text)
    else:
        return

def parse_json(data):
    try:
        dssfile = HecDss.open(r"C:\Users\u4rs9jsg\Documents\github_repos\ns5-acp\mydss.dss")
        tsc = TimeSeriesContainer()
        tsc.fullName = "/Panama/Gatun Lake/Elev//15Minute//"


        ts = data["ts"]
        units = ts["units"]
        if units == "pies": units = "ft"
        
        values = []
        times = []

        ts_data = ts["data"]
        for d in ts_data:
            times.append(HecTime(d.get("dt")).value())
            values.append(d.get("v"))

        tsc.times = times
        tsc.values = values
        tsc.numberValues = len(values)
        tsc.units = units
        tsc.type = "INST-VAL"
        dssfile.put(tsc)
    except Exception, e:
        msg = " ".join(e.args)
        print(e)
        # MessageBox.showError(msg, "DSS Error")

    # for o in data:
        # if o["numId"] == 54: print(o)
        # if o["locId"].startswith("54"): print(o)
        # print(o)

if __name__ =="__main__" or __name__=="main":
    host = "https://panama-cloud-ns5.trilynx-novastar.systems/novastar/data/api/v1"
    # endpoint="stations"
    endpoint="ts"
    query_params = urllib.urlencode({
    "dataService" : "data",
    # "debug" : "false",
    "flag" : "*",
    "format":"json",
    # "includeEstimates" : "false",
    # "includeMissing" : "false",
    # "includeProfile" : "false",
    "includeReports" : "true",
    "periodStart":"now_minus_7Days",
    "periodEnd":"now",
    "readData" : "true",
    "tsid":"54-5400.NovaStar5.WaterLevelRiver-Mean.15Minute"
    })

    endpoint_path = "%s/%s?%s" % (host, endpoint, query_params)
    # print(endpoint_path)

    res = fetch_data(endpoint_path)

    if res is not None:
        parse_json(res)
