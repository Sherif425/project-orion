try:
    with open("missing.txt", "r", encoding="utf-8") as file:
        print(file.read())
except FileNotFoundError as error:
    print("Error: The file 'missing.txt' was not found.")
    print(error)