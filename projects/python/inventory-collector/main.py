from pprint import pprint
from datetime import datetime
import platform
from inventory.osinfo import get_os_info
from inventory.cpu import get_cpu_info
from inventory.writer import write_inventory
from inventory.logging_config import configure_logging
from inventory.memory import get_memory_info
from inventory.disk import get_disk_info
from inventory.network import get_network_info
from inventory.config import load_config
from inventory.cli import parse_arguments

def main() -> None:

    configure_logging()
    config = load_config()
    args = parse_arguments()

    output_file = (
        args.output
        if args.output
        else config["collector"]["output_file"]
    )

    # inventory = {
    #     "metadata": {
    #     "generated_at": datetime.now().isoformat(timespec="seconds"),
    #     "collector_version": config["collector"]["version"],
    #     "python_version": platform.python_version(),
    #     },
    #     "os": get_os_info(),
    #     "cpu": get_cpu_info(),
    #     #"bad": object(),  was embedded to test logging
    #     "memory": get_memory_info(),
    #     "disk": get_disk_info(),
    #     "network": get_network_info(),
    # }

    inventory = {}
    if config["features"]["collect_os"]:
        inventory["os"] = get_os_info()
    if config["features"]["collect_cpu"]:
        inventory["cpu"] = get_cpu_info()
    if config["features"]["collect_memory"]:
        inventory["memory"] = get_memory_info()
    if config["features"]["collect_disk"]:
        inventory["disk"] = get_disk_info()
    if config["features"]["collect_network"]:
        inventory["network"] = get_network_info()

    pprint(inventory)

    write_inventory(
        inventory,
        output_file=output_file,
    )
    

if __name__ == "__main__":
    main()
