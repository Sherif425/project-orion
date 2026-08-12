import inspect
import json
from pathlib import Path
import psutil

print("\n")
print(inspect.signature(json.dump))
print("\n")
print(inspect.signature(Path.open))
print("\n")
print(inspect.signature(psutil.cpu_percent))
print("\n")
print(inspect.signature(psutil.cpu_count))