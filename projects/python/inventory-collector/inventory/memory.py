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
from inventory.utils import bytes_to_gb

def get_memory_info() -> dict[str, Any]:
    """
    Collect Memory information
    """

    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        "virtual":{
            "total_gb": bytes_to_gb(vm.total),
            "available_gb": bytes_to_gb(vm.available),
            "used_gb": bytes_to_gb(vm.used),
            "usage_percent": vm.percent,
        },
        "swap":{
            "total_gb": bytes_to_gb(swap.total),
            "used_gb": bytes_to_gb(swap.used),
            "usage_percent": swap.percent,
        },
    }