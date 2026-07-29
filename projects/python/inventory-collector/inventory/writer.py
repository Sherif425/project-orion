import json


def write_inventory(data, filename="inventory.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)