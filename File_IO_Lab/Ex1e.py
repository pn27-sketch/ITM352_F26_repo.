file = open("names.txt", mode="r", encoding="utf-8")
names = [line.strip() for line in file.readlines()]
file.close()

for name in names:
    print(name)

print(f"Total names: {len(names)}")