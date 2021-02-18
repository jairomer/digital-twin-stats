#!/usr/bin/python3 

from pathlib import Path 
from pandas import DataFrame, read_csv
import pandas as pd
import matplotlib.pyplot as plot
from location import DataPath 

def loadDataset(RealTime : bool, Speed : int):
    path = DataPath.getCsvPath(RealTime, Speed)
    file = Path(path)
    if not file.is_file():
        raise FileNotFoundError("Not a file: "+path) 

    # Read CSV with pandas and return it.
    dt = pd.read_csv(file, sep=",")
    dt = dt.rename(columns={" turn_around_time" : "tat"})
    dt.set_index(['id'], inplace=True)

    # Clean outliers
    dt["tat"] = pd.DataFrame(filter(lambda x: x < 150, dt["tat"]))

    return dt

def getBoxPlotCategory(RealTime : bool):
    speeds = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
    ylabel = "Response latency in milliseconds"
    xlabel = ""
    if RealTime:
        xlabel = "Speeds in real-time mode"
    else:
        xlabel = "Speeds in non-real mode"

    category = pd.DataFrame()

    for spd in speeds:
        meas = loadDataset(RealTime=RealTime, Speed=spd)
        category["speed "+str(spd)] = meas["tat"]
    
    category.plot.box(grid=True, figsize=(10, 6))
    plot.gca().set(xlabel=xlabel, ylabel=ylabel)
    plot.savefig(DataPath.getBoxCategoryPath(RealTime))
    plot.close()


def plotBoxForIcmpPing():
    path = DataPath.getPingLatencyDataset()
    file = Path(path)
    if not file.is_file():
        raise FileNotFoundError("Not a file: "+path) 
    dataset = pd.read_csv(file, sep=",")
    dataset.plot.box(grid=True, figsize=(10, 6))
    plot.gca().set(
        ylabel="Latency in milliseconds", 
        xlabel="Wifi Link Latency")

    plot.savefig(DataPath.getPingBoxPlotPath())
    plot.close()

if __name__ == '__main__':
    print ("Obtaining box plots...",)
    getBoxPlotCategory(RealTime=True)
    getBoxPlotCategory(RealTime=False)
    plotBoxForIcmpPing()