import os

class DataPath: 
    def getCsvPath(RealTime : bool, Speed : int):
        NotRT   = "Non Real Time"
        RT      = "Real Time"
        template    = os.getcwd()+"/data/{}/Pro/latency_wifi_speed_{}.csv" 
        path        = ""
        if RealTime:
            return template.format(RT, Speed)
        else:
            return template.format(NotRT, Speed)

    def getBoxPlotPath(RealTime : bool, Threaded : bool, Speed : int):
        NotRT   = "Non Real Time"
        RT      = "Real Time"
        template    = os.getcwd()+"/data/{}/Pro/latency_wifi_speed_{}.png" 
        path        = ""
        if RealTime:
            return template.format(RT, Speed)
        else:
            return template.format(NotRT, Speed)

    def getBoxCategoryPath(RealTime : bool):
        NotRT   = "Non Real Time"
        RT      = "Real Time"
        template    = os.getcwd()+"/data/{}/Pro/box_{}.png" 
        path        = ""
        if RealTime:
            return template.format(RT, RealTime)
        else:
            return template.format(NotRT, RealTime)

    def getPingLatencyDataset(): 
        return "data/ping/ping.csv"
        
    def getPingBoxPlotPath():
        return "data/ping/ping.png"
