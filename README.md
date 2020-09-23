
# Latency measurements between a CoppeliaSim simulator and a ROS node over a WiFi network.

## What is this? 
The purpose of this repository is to store the code and data used to analyze a set of latency measurements between a simulation in CoppeliaSim with different settings and a ROS node in order to identify the best configuration for real-time behaviour. 

Plots and dataframes can be found on directory `data`.

## How to run it?
To use this scripts, you will need to load a Python3 virtual environment and install the requirements:
```bash
cd digital-twin-stats
python3 -m venv virtualenv
source virtualenv/bin/activate 
virtualenv/bin/pip3 install -r requirements.txt
``` 

The tune the script on `src/analisis.py` to get what you want.  

Then run script `./run` and enjoy or suffer the results of your actions. 

