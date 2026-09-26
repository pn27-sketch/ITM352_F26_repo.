durations = [1.1, 0.8, 2.5, 2.6]
costs = ("$6.25", "$5.25", "$10.50", "$8.05")

trips = {
    "fares": costs, 
    "miles": durations
}

print(trips)
print(f"The 3rd trip miles: {trips['miles'][2]} and trip cost: {trips['fares'][2]}")