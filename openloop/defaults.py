from datetime import datetime
import psutil
import openloop as openloop

global cpu_hist
cpu_hist = []
def cpu_str():
    val = psutil.cpu_percent()
    if val == 0 or val == 100:
        val = cpu_hist[len(cpu_hist)-1]
    else:
        cpu_hist.append(val)
    return str(val)+"%"

def cpu_temperature():
    temp_data = psutil.sensors_temperatures()
    return str(temp_data["cpu_thermal"][0].current) + chr(176) + "C"
    
def debug_test():
    print("Called debug test")
    return "https://stackoverflow.com"

def comp_time():
    time = datetime.now().time()
    return f"{time.hour}:{time.minute}:{time.second}"

def version():
    return f"{openloop.num}-{openloop.code}"

package = {
    "time": datetime.now,
    "timec": comp_time,
    "cpu": cpu_str,
    "cpu_temp": cpu_temperature,
    "debug": debug_test,
    "version": version
}