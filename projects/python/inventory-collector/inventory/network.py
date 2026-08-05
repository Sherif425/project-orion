# import socket
# from typing import Any


# def get_network_info() -> dict["str", Any]:
#     """
#     Collect basic Network Information.

#     Returns:
#         Dictionary containing network details.
#     """
#     hostname = socket.gethostname()

#     return {
#         "hostname": hostname,
#         "fqdn": socket.getfqdn(),
#         "ip_address": socket.gethostbyname(hostname),
#     }

# Update network module using psutil
import socket
import psutil
from typing import Any


def get_network_info() -> dict[str, Any]:
    """Collect network information"""


    return {
        "hostname": socket.gethostname(),
        "FQDN": socket.getfqdn(),
        "interfaces": list(psutil.net_if_addrs().keys()),
        "network_stats": {
            name: stats.isup
            for name, stats in psutil.net_if_stats().items()
        },
    }