import socket
from typing import Any


def get_network_info() -> dict["str", Any]:
    """
    Collect basic Network Information.

    Returns:
        Dictionary containing network details.
    """
    hostname = socket.gethostname()

    return {
        "hostname": hostname,
        "fqdn": socket.getfqdn(),
        "ip_address": socket.gethostbyname(hostname),
    }