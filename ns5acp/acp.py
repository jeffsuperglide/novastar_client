""" _summary_
"""

import urllib
import urllib2
import json



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
    ts = data["ts"]
    ts_data = ts["data"]

    for d in ts_data:
        print(d)

    # for o in data:
        # if o["numId"] == 54: print(o)
        # if o["locId"].startswith("54"): print(o)
        # print(o)

if __name__ =="__main__" or __name__=="main":
    host = "https://panama-cloud-ns5.trilynx-novastar.systems/novastar/data/api/v1"
    # endpoint="stations"
    endpoint="ts"
    # query_params = urllib.urlencode({
    #     "dataType":"WaterLevelRiver,WaterLevelRiverMin,WaterLevelRiverMax",
    #     "debug":"false",
    #     "format":"json",
    #     "formatPrettyPrint":"false",
    #     "includeRetiredStations":"false",
    #     "includeTestStations":"false",
    #     "jsonFormat":"bare",
    #     "outOfService":"false",
    #     "xmlFormat":"full"
    # })
        # dataInterval=%2A,
        # dataType=%2A,
        # "debug" : "false",
        # "includeAlarmTs" : "true",
        # "includeCalibrationTs" : "true",
        # "includeNovaScoreTs" : "true",
        # "includeProblemTs" : "true",
        # "includeRatedTs" : "true",
        # "includeRatingTs" : "true",
        # "includeRawTs" : "true",
        # "includeScaledTs" : "true",
        # "includeStandardCalculatedIntervalTs" : "true",
        # "xmlFormat" : "full"
    # query_params = urllib.urlencode({
    #     "format" : "json",
    #     "formatPrettyPrint" : "false",
    #     "jsonFormat" : "bare",
    #     "locId" : "54-*",
    # })
    query_params = urllib.urlencode({
    "dataService" : "data",
    "debug" : "false",
    "flag" : "*",
    "format":"json",
    "includeEstimates" : "false",
    "includeMissing" : "false",
    "includeProfile" : "false",
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
