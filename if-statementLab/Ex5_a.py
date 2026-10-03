def celsius_to_fahrenheit(celsius):
	assert celsius >= -273.15, "Temperature cannot be below absolute zero."
	return celsius * 9 / 5 + 32