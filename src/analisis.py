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


def getDataPath(RealTime : bool, Threaded : bool, Speed : int):
    NotRT   = "Non Real Time"
    RT      = "Real Time"
    NotThr  = "Non Threaded"
    Thr     = "Threaded" 
    template    = os.getcwd()+"/data/{}/{}/latency_wifi_speed_{}.csv" 
    path        = ""
    if RealTime:
        if Threaded:
            path = template.format(RT, Thr, Speed)
        else:
            path = template.format(RT, NotThr, Speed)
    else:
        if Threaded: 
            path = template.format(NotRT, Thr, Speed)
        else:
            path = template.format(NotRT, NotThr, Speed)
    
    return path

def getBoxPlotPath(RealTime : bool, Threaded : bool, Speed : int):
    NotRT   = "Non Real Time"
    RT      = "Real Time"
    NotThr  = "Non Threaded"
    Thr     = "Threaded" 
    template    = os.getcwd()+"/data/{}/{}/latency_wifi_speed_{}.png" 
    path        = ""
    if RealTime:
        if Threaded:
            path = template.format(RT, Thr, Speed)
        else:
            path = template.format(RT, NotThr, Speed)
    else:
        if Threaded: 
            path = template.format(NotRT, Thr, Speed)
        else:
            path = template.format(NotRT, NotThr, Speed)
    
    return path

def getBoxCategoryPath(RealTime : bool, Threaded : bool):
    NotRT   = "Non Real Time"
    RT      = "Real Time"
    NotThr  = "Non Threaded"
    Thr     = "Threaded" 
    template    = os.getcwd()+"/data/{}/{}/box_{}{}.png" 
    path        = ""
    if RealTime:
        if Threaded:
            path = template.format(RT, Thr, RealTime, Threaded)
        else:
            path = template.format(RT, NotThr, RealTime, Threaded)
    else:
        if Threaded: 
            path = template.format(NotRT, Thr, RealTime, Threaded)
        else:
            path = template.format(NotRT, NotThr, RealTime, Threaded)
    
    return path

def getChartCategoryPath(RealTime : bool, Threaded : bool):
    NotRT   = "Non Real Time"
    RT      = "Real Time"
    NotThr  = "Non Threaded"
    Thr     = "Threaded" 
    template    = os.getcwd()+"/data/{}/{}/chart_{}{}.png" 
    path        = ""
    if RealTime:
        if Threaded:
            path = template.format(RT, Thr, RealTime, Threaded)
        else:
            path = template.format(RT, NotThr, RealTime, Threaded)
    else:
        if Threaded: 
            path = template.format(NotRT, Thr, RealTime, Threaded)
        else:
            path = template.format(NotRT, NotThr, RealTime, Threaded)
    
    return path

def loadDataset(RealTime : bool, Threaded : bool, Speed : int):
    file = Path(getDataPath(RealTime, Threaded, Speed))
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
        for rt, thr in (True, False):
            tt = loadDataset(RealTime=rt, Threaded=thr, Speed=spd)
            plot.ylabel("ms")
            tt.plot.box(grid=True)
            plot.savefig(getBoxPlotPath(RealTime=rt, Threaded=thr, Speed=spd))
            plot.clf() 
            print(".",)
        
    plot.close('all')

def getXLabel(RealTime : bool, Threaded : bool):
    if RealTime:
        if Threaded:
            return "Realtime/Threaded"
        else:
            return "Realtime/Non-Threaded"
    else:
        if Threaded:
            return "Non-Realtime/Threaded"
        else:
            return "Non-Realtime/NonThreaded"

def getBoxPlotCategory(RealTime : bool, Threaded : bool):
    speeds = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
    plot.ylabel("ms")
    plot.xlabel(getXLabel(RealTime, Threaded))

    category = pd.DataFrame()
    for spd in speeds:
        meas = loadDataset(RealTime=RealTime, Threaded=Threaded, Speed=spd)
        category["speed "+str(spd)] = meas["tat"]

    category.plot.box(grid=True, figsize=(10, 6))
    plot.savefig(getBoxCategoryPath(RealTime, Threaded))
    plot.close('all')

def printStdDevPerCategory(RealTime : bool, Threaded : bool):
    speeds = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
    print(getXLabel(RealTime, Threaded))
    for spd in speeds:
        meas = loadDataset(RealTime=RealTime, Threaded=Threaded, Speed=spd)
        print("speed " + str(spd) + ": \t" + str(meas["tat"].std()))
    print("-------------")

def getStdDeviationHistogramsPerCategory(RealTime : bool, Threaded : bool):
    speeds = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
    deviations = []
    indx = []
    for spd in speeds:
        deviations.append(loadDataset(RealTime=RealTime, Threaded=Threaded, Speed=spd)["tat"].std())
        indx.append(str(spd))
    stdplot = pd.DataFrame({"std" : deviations}, index=indx)
    plot.title(getXLabel(RealTime, Threaded))
    plot.xlabel("Speed")
    plot.ylabel("ms")
    stdplot["std"].plot.bar()
    plot.savefig(getChartCategoryPath(RealTime, Threaded))
    plot.close('all')


        

def main():
    for rt, thr in [ (i,j) for i in (True, False) for j in (True, False)]:
        #getBoxPlotCategory(rt, thr)
        #printStdDevPerCategory(rt, thr)
        getStdDeviationHistogramsPerCategory(rt, thr)

if __name__ == '__main__':
    main() 
