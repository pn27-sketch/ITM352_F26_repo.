import pandas as pd
from sodapy import Socrata


client = Socrata("data.cityofchicago.org", None)
records = client.get("rr23-ymwb", limit=500)
vehicles = pd.DataFrame.from_records(records)

print(vehicles.head())

print(vehicles[["vehicle_type", "vehicle_fuel_source"]].to_string(index=False))

print("\nVehicle counts by fuel source:")
print(vehicles.groupby("vehicle_fuel_source", dropna=False).size())