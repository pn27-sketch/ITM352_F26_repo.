import ssl

import pandas as pd


url = (
    "https://home.treasury.gov/resource-center/data-chart-center/"
    "interest-rates/TextView?type=daily_treasury_yield_curve"
    "&field_tdr_date_value_month=202603"
)

ssl._create_default_https_context = ssl._create_unverified_context

tables = pd.read_html(url)
interest_rates = tables[0]
print(interest_rates.columns)

for _, row in interest_rates.iterrows():
    print(row["1 Mo"])