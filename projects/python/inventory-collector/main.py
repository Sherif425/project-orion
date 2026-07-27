from pprint import pprint
from inventory.osinfo import get_os_info
from inventory.cpu import get_cpu_info


def main():
    inventory = {
        "os": get_os_info(),
        "cpu": get_cpu_info(),
    }


    pprint(inventory)
    

if __name__ == "__main__":
    main()
