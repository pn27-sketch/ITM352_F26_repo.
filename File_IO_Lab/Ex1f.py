with open("names.txt", mode="r", encoding="utf-8") as file:
    contents = file.read()

if not contents.splitlines() or contents.splitlines()[-1] != "Patrick":
    with open("names.txt", mode="a", encoding="utf-8") as file:
        if contents and not contents.endswith("\n"):
            file.write("\n")
        file.write("Patrick\n")

with open("names.txt", mode="r", encoding="utf-8") as file:
    print(file.read(), end="")