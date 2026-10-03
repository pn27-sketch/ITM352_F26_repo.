def isLeapYear(year):
	if year % 400 == 0:
		return "Leap year"
	elif year % 100 == 0:
		return "Not a leap year"
	elif year % 4 == 0:
		return "Leap year"
	else:
		return "Not a leap year"


def is_leap_year_expression(year):
	return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def closest_leap_year(year):
	for distance in range(5):
		earlier_year = year - distance
		later_year = year + distance

		if earlier_year > 0 and is_leap_year_expression(earlier_year):
			return earlier_year
		if is_leap_year_expression(later_year):
			return later_year


birth_year = 2006
nearest_leap_year = closest_leap_year(birth_year)
test_years = [birth_year]

if nearest_leap_year != birth_year:
	test_years.append(nearest_leap_year)

if is_leap_year_expression(birth_year):
	test_years.append(birth_year + 1)

for year in test_years:
	expression_result = is_leap_year_expression(year)
	function_result = isLeapYear(year)
	print(f"{year}: {function_result} (expression: {expression_result})")