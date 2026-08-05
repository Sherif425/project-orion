# import os

# def get_cpu_info():
#     return {
        
#         "logical_cores": os.cpu_count() 
#     }

import psutil
from typing import Any


def get_cpu_info() -> dict[str, Any]:
    """
    Collect CPU Info
    """
    freq = psutil.cpu_freq()

    return {
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "usage_percent": psutil.cpu_percent(interval=1),
        "frequency": {
            "current_mhz": round(freq.current, 2) if freq else None,
            "min_hhz": round(freq.min, 2) if freq else None,
            "max_freq": round(freq.max, 2) if freq else None,
        },

    }
