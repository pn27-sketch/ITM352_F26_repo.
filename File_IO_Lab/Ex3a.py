import csv

total_fares = 0.0
trip_count = 0
maximum_trip_miles = 0.0

with open("taxi_1000.csv", mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        fare = row.get("Fare")
        trip_miles = row.get("Trip Miles")

        if fare:
            total_fares += float(fare)
            trip_count += 1

        if trip_miles:
            maximum_trip_miles = max(maximum_trip_miles, float(trip_miles))

average_fare = total_fares / trip_count

print(f"Total fares: ${total_fares:,.2f}")
print(f"Average fare: ${average_fare:,.2f}")
print(f"Maximum trip distance: {maximum_trip_miles:,.2f} miles")