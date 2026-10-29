file = open("names.txt", mode="r", encoding="utf-8")
names_text = file.read()
file.close()

names = names_text.splitlines()

for name in names:
    print(name)

print(f"Total names: {len(names)}")