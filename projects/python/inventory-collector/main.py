from pprint import pprint
from inventory.osinfo import get_os_info
from inventory.cpu import get_cpu_info
from inventory.writer import write_inventory
from inventory.logging_config import configure_logging
from inventory.memory import get_memory_info
from inventory.disk import get_disk_info
from inventory.network import get_network_info
def main() -> None:

    configure_logging()

    inventory = {
        "os": get_os_info(),
        "cpu": get_cpu_info(),
        #"bad": object(),  was embedded to test logging
        "memory": get_memory_info(),
        "disk": get_disk_info(),
        "network": get_network_info(),
    }

    pprint(inventory)

    write_inventory(inventory)
    

if __name__ == "__main__":
    main()
