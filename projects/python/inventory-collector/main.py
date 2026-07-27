from pprint import pprint
from inventory.osinfo import get_os_info


def main():
    inventory = get_os_info()
    pprint(inventory)
    

if __name__ == "__main__":
    main()
