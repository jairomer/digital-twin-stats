#!/usr/bin/python3 
"""
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██░████░▄▄▀█▄░▄█░▄▄█░▄▄▀█▀▄▀█░██░███░▄▄▀█░▄▄▀█░▄▄▀█░██░██░█░▄▄██▄██░▄▄█
██░████░▀▀░██░██░▄▄█░██░█░█▀█░▀▀░███░▀▀░█░██░█░▀▀░█░██░▀▀░█▄▄▀██░▄█▄▄▀█
██░▀▀░█▄██▄██▄██▄▄▄█▄██▄██▄██▀▀▀▄███░██░█▄██▄█▄██▄█▄▄█▀▀▀▄█▄▄▄█▄▄▄█▄▄▄█
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

Variables:
 - Theraded Mode: yes/No
 - Realtime Mode: yes/no
 - Speeds: [-3,-2,-1,0,1,2,3,4,5,6]

Dataset: 
 - ID
 - Latency

To Obtain: 
 - Sparsiness of the latency per dataset, measurements of variability.
 - Average and median latency per dataset. 
 - Box diagram for each dataset. 
 - Distribution of latency points per dataset.

We want to measure stability and predictability of the connection in order to choose the 
most stable configuration.

PROCESS: 
 Step 1: Read all datasets.  
 Step 2: ??? 
 Step 3: For each dataset obtain the average, median latency and sparsiness.  
 Step 4: Return the 3 least sparse and with lower median configurations.
 Step 5: Generate Box diagram for each dataset. 
 Step 6: Compare best datasets for each RT/Threaded category:
  - Obtain box diagram. 
  - Obtain point diagram.  
 Step 7: Store diagrams on disk.
"""

import os
from pathlib import Path 
from pandas import DataFrame, read_csv
import pandas as pd
import matplotlib.pyplot as plot


def getDataPath(RealTime : bool, Speed : int):
    NotRT   = "Non Real Time"
    RT      = "Real Time"
    template    = os.getcwd()+"/data/{}/Pro/latency_wifi_speed_{}.csv" 
    path        = ""
    if RealTime:
        path = template.format(RT, Speed)
    else:
        path = template.format(NotRT, Speed)
    return path

def getBoxPlotPath(RealTime : bool, Threaded : bool, Speed : int):
    NotRT   = "Non Real Time"
    RT      = "Real Time"
    template    = os.getcwd()+"/data/{}/Pro/latency_wifi_speed_{}.png" 
    path        = ""
    if RealTime:
        path = template.format(RT, Speed)
    else:
        path = template.format(NotRT, Speed)
    
    return path

def getBoxCategoryPath(RealTime : bool):
    NotRT   = "Non Real Time"
    RT      = "Real Time"
    template    = os.getcwd()+"/data/{}/Pro/box_{}.png" 
    path        = ""
    if RealTime:
        path = template.format(RT, RealTime)
    else:
        path = template.format(NotRT, RealTime)
    
    return path

def getChartCategoryPath(RealTime : bool):
    NotRT   = "Non Real Time"
    RT      = "Real Time"
    template    = os.getcwd()+"/data/{}/Pro/chart_{}.png" 
    path        = ""
    if RealTime:
        path = template.format(RT, RealTime)
    else:
        path = template.format(NotRT, RealTime)
    
    return path

def loadDataset(RealTime : bool, Speed : int):
    file = Path(getDataPath(RealTime, Speed))
    if not file.is_file():
        raise FileNotFoundError("Not a file: "+path) 

    # Read CSV with pandas and return it.
    dt = pd.read_csv(file, sep=",")
    dt = dt.rename(columns={" turn_around_time" : "tat"})
    dt.set_index(['id'], inplace=True)

    # Clean outliers
    dt["tat"] = pd.DataFrame(filter(lambda x: x < 150, dt["tat"]))

    return dt

def obtainAllBoxPlots():
    speeds = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
    plot.ylabel("ms")

    for spd in speeds:
        for rt in (True, False):
            tt = loadDataset(RealTime=rt, Speed=spd)
            plot.ylabel("ms")
            tt.plot.box(grid=True)
            plot.savefig(getBoxPlotPath(RealTime=rt, Speed=spd))
            plot.clf() 
            print(".",)

    plot.close('all')

def getXLabel(RealTime : bool):
    if RealTime:
            return "Realtime"
    else:
            return "Non-Realtime"

def getBoxPlotCategory(RealTime : bool):
    speeds = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
    plot.ylabel("ms")
    plot.xlabel(getXLabel(RealTime))

    category = pd.DataFrame()
    for spd in speeds:
        meas = loadDataset(RealTime=RealTime, Speed=spd)
        category["speed "+str(spd)] = meas["tat"]

    category.plot.box(grid=True, figsize=(10, 6))
    plot.savefig(getBoxCategoryPath(RealTime))
    plot.close('all')

def printStdDevPerCategory(RealTime : bool):
    speeds = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
    print(getXLabel(RealTime, Threaded))
    for spd in speeds:
        meas = loadDataset(RealTime=RealTime, Speed=spd)
        print("speed " + str(spd) + ": \t" + str(meas["tat"].std()))
    print("-------------")

def getStdDeviationHistogramsPerCategory(RealTime : bool):
    speeds = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
    deviations = []
    indx = []
    for spd in speeds:
        deviations.append(loadDataset(RealTime=RealTime, Speed=spd)["tat"].std())
        indx.append(str(spd))
    stdplot = pd.DataFrame({"std" : deviations}, index=indx)
    plot.title(getXLabel(RealTime))
    plot.xlabel("Speed")
    plot.ylabel("ms")
    stdplot["std"].plot.bar()
    plot.savefig(getChartCategoryPath(RealTime))
    plot.close('all')

def getPingLatencyDataset(): 
    file = Path("data/ping/ping.csv")
    if not file.is_file():
        raise FileNotFoundError("Not a file: "+path) 

    # Read CSV with pandas and return it.
    dt = pd.read_csv(file, sep=",")
    return dt

def plotBoxPing(dataset):
    plot.ylabel("ms")
    plot.xlabel("Wifi Link Latency")
    dataset.plot.box(grid=True, figsize=(10, 6))
    plot.savefig("data/ping")
    plot.close('all')

def printPingStatistics(dataset): 
    # Get Average. 
    print("Wifi ping average: {}".format(dataset["ms"].mean()))
    # Get Middle
    print("Wifi ping median: {}".format(dataset["ms"].median()))
        
def main():
    print ("Obtaining box and histograms...",)
    for rt in [True, False]:
        print(".",)
        getBoxPlotCategory(rt)
        getStdDeviationHistogramsPerCategory(rt)
    
    link_lat = getPingLatencyDataset()
    plotBoxPing(link_lat)
    printPingStatistics(link_lat)


if __name__ == '__main__':
    main() 
