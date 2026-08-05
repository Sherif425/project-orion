import psutil
from pathlib import Path
from shutil import disk_usage
from typing import Any
from inventory.utils import bytes_to_gb

def get_disk_info() -> dict["str", Any]:
    """
    Collect Disk usage information for the current drive.

    Returns:
        Dictionary containing Disk details.
    """

    # root = Path.cwd().anchor #or "/"

    # usage = disk_usage(root)

    # return {
    #     "path": root,
    #     "total_gb": round(usage.total / (1024 ** 3), 2),
    #     "used_gb": round(usage.used / (1024 ** 3), 2),
    #     "free_gb": round(usage.free / (1024 ** 3), 2),
    # }

    partitions = []

    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)

            partitions.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "filesystem": partition.fstype,
                "total_gb": bytes_to_gb(usage.total),
                "free_gb": bytes_to_gb(usage.free),
                "used_gb": bytes_to_gb(usage.used),
                "usage_percent": usage.percent,
            })
        except PermissionError:
            continue

    return {"partitions": partitions}