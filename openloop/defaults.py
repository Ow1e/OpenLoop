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

global cpu_temp_enabled
cpu_temp_enabled = True
def cpu_temperature():
    if cpu_temp_enabled:
        try:
            if "sensors_temperatures" in dir(psutil):
                temp_data = psutil.sensors_temperatures()
                return str(temp_data["cpu_thermal"][0].current) + chr(176) + "C"
            else:
                return "Unsupported"
        except:
            return "Error"
    else:
        return "Disabled"

def ram_usage():
    ram_used = psutil.virtual_memory().percent
    return str(ram_used) + "%"


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
    "ram_used": ram_usage,
    "debug": debug_test,
    "version": version
}