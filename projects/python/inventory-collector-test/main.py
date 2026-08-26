from pprint import pp
import os
import shutil
import psutil
from win32con import TRUE, FALSE

cpu_cores = os.cpu_count()
pp(cpu_cores)
print("cpu cores : ", cpu_cores)

disk_info = shutil.disk_usage("/")
pp(f"Total Disk:  {disk_info.total / (1024 ** 3): .2f} GB" )
pp(f"Used Disk:  {disk_info.used / (1024 ** 3): .2f} GB" )
pp(f"Free Disk:  {disk_info.free / (1024 ** 3): .2f} GB" )


print("---CPU---")
print(f"Physicl cores: {psutil.cpu_count(logical= FALSE)}")
print(f"logicl cores: {psutil.cpu_count(logical= TRUE)}")
print(f"Current CPU Usage: {psutil.cpu_percent(interval=1)}%")

print("---Disk---")
disk_usage = psutil.disk_usage("/")
print(f"Total Space: {disk_usage.total / (1024 ** 3): .2f} GB")
print(f"Free Space: {disk_usage.free / (1024 ** 3): .2f} GB")
print(f"Total Usage Percentage: {disk_usage.percent}%")
