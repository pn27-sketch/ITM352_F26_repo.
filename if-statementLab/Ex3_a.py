age = 67
weekday = "Tuesday"
matinee = True

price = 14

if age >= 65:
	price = min(price, 8)

if weekday.lower() == "tuesday":
	price = min(price, 10)

if matinee:
	matinee_price = 5 if age >= 65 else 8
	price = min(price, matinee_price)

print("Age:", age)
print("Weekday:", weekday)
print("Matinee:", matinee)
print("Movie price: $" + str(price))