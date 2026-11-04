from pathlib import Path

import pandas as pd


homes = pd.read_csv(Path(__file__).with_name("homes_data.csv"))

print("DataFrame dimensions (rows, columns):")
print(homes.shape)

print("\nFirst 10 rows:")
print(homes.head(10).to_string(index=False))

large_properties = homes.loc[homes["units"] >= 500].drop(
    columns=["id", "borough", "block", "lot", "easement"]
).copy()

print("\nProperties with 500 or more units (first 10 rows):")
print(large_properties.head(10))

print("\nData types before conversion:")
print(large_properties.dtypes)

numeric_columns = ["units", "land_sqft", "gross_sqft", "year_built", "sale_price"]
for column in numeric_columns:
    large_properties[column] = pd.to_numeric(
        large_properties[column], errors="coerce"
    ).astype("Int64")

print("\nData types after conversion:")
print(large_properties.dtypes)
print("\nData after type conversion:")
print(large_properties)

clean_properties = large_properties.dropna().drop_duplicates()
print("\nAfter dropping rows with null values and duplicates:")
print(clean_properties)

properties_with_sales = clean_properties.loc[clean_properties["sale_price"] != 0]
print("\nAfter filtering out zero sales:")
print(properties_with_sales)

print("\nAverage sales price:")
print(properties_with_sales["sale_price"].mean())