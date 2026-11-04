from pathlib import Path

import pandas as pd


taxi_trips = pd.read_json(Path(__file__).with_name("Taxi_Trips.json"))

print("Taxi trips:")
print(taxi_trips)

print("\nSummary statistics:")
print(taxi_trips.describe(include="all"))

print("\nMedian:")
print(taxi_trips.median(numeric_only=True))