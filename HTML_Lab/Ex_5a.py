import pandas as pd
import requests


URL = (
    "https://data.cityofchicago.org/resource/97wa-y6ff.json"
    "?$select=driver_type,count(license)&$group=driver_type"
)

response = requests.get(URL)
response.raise_for_status()
records = response.json()

print(records)
print("Data format:", type(records).__name__)

licenses_by_driver = pd.DataFrame(records).rename(
    columns={"count_license": "count"}
)
licenses_by_driver = licenses_by_driver[["count", "driver_type"]]
licenses_by_driver = licenses_by_driver.set_index("driver_type")
print(licenses_by_driver)