durations = [1.1, 0.8, 2.5, 2.6]
costs = ("$6.25", "$5.25", "$10.50", "$8.05")

trips = {
    "fares": costs, 
    "miles": durations
}

#c.	Look up the zip()function and use it to create a dictionary where the keys are the durations and the values are the fares. You will need to use dict() to create the dictionary from the return value of zip(). Print out the duration and cost of the 3rd trip. 
trip_dict = dict(zip(durations, costs))

print(trips)
print(f"The 3rd trip duration: {durations[2]} and trip cost: {trip_dict[durations[2]]}")