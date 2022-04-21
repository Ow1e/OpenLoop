from datetime import datetime
import psutil

global cpu_hist
cpu_hist = []
def cpu_str():
    val = psutil.cpu_percent()
    if val == 0 or val == 100:
        val = cpu_hist[len(cpu_hist)-1]
    else:
        cpu_hist.append(val)
    return str(val)+"%"

def debug_test():
    print("Called debug test")
    return "https://stackoverflow.com"

def comp_time():
    time = datetime.now().time()
    return f"{time.hour}:{time.minute}:{time.second}"

package = {
    "time": datetime.now,
    "timec": comp_time,
    "cpu": cpu_str,
    "debug": debug_test
}