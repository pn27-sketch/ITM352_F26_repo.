durations = [1.1, 0.8, 2.5, 2.6]
costs = (6.25, 5.25, 10.50, 8.05)

trips = {
	"fares": costs,
	"miles": durations
}

trip_dict = dict(zip(durations, costs))
third_duration = durations[2]

print(trips)
print(f"The 3rd trip duration: {third_duration} and trip cost: ${trip_dict[third_duration]:.2f}")

# Numeric fares are better for calculations; currency formatting belongs in the output.