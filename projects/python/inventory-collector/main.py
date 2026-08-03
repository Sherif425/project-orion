from pprint import pprint
from inventory.osinfo import get_os_info
from inventory.cpu import get_cpu_info
from inventory.writer import write_inventory

def main():
    inventory = {
        "os": get_os_info(),
        "cpu": get_cpu_info(),
        "bad": object,
        
    }


    pprint(inventory)

    write_inventory(inventory)
    

if __name__ == "__main__":
    main()
