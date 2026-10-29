file = open("names.txt", mode="r", encoding="utf-8")
names = []

line = file.readline()
while line:
    names.append(line.strip())
    line = file.readline()

file.close()

for name in names:
    print(name)

print(f"Total names: {len(names)}")