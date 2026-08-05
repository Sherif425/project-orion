# import platform
# from typing import Any

# def get_memory_info() -> dict["str", Any]:
#     """
#     Collect Memory Information.

#     Returns:
#         Dictionary containing memory details.
#     """


#     return {
#         "status": "Available in Sprint 02",
#         "platform": platform.system(),
#         "note": (
#             "Detailed memory statistics require platform-specific "
#             "APIs or the psutil package."
#         ),

#     }

# memory module using psutil
import psutil
from typing import Any

def get_memory_info() -> dict[str, Any]:
    """
    Collect Memory information
    """

    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        "virtual":{
            "total_gb": round(vm.total / (1024**3), 2),
            "available_gb": round(vm.available / (1024 **3), 2),
            "used_gb": round(vm.used /(1024 ** 3), 2),
            "usage_percent": vm.percent,
        },
        "swap":{
            "total_gb": round(swap.total / (1024**3), 2),
            "used_gb": round(swap.used / (1024**3), 2),
            "usage_percent": swap.percent,
        },
    }