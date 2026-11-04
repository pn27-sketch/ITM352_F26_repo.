from pathlib import Path

import numpy as np
import pandas as pd


csv_path = Path(__file__).with_name("sales_data.csv")

try:
    sales = pd.read_csv(
        csv_path,
        dtype_backend="pyarrow",
        on_bad_lines="skip",
        parse_dates=["order_date"],
        date_format="mixed",
    )
except FileNotFoundError as error:
    raise FileNotFoundError(f"Sales CSV file was not found: {csv_path}") from error
except ImportError as error:
    raise ImportError(
        "Reading with the PyArrow data type backend requires the pyarrow package."
    ) from error
except pd.errors.ParserError as error:
    raise pd.errors.ParserError(
        f"Could not parse the sales CSV file: {csv_path}"
    ) from error

sales["quantity"] = pd.to_numeric(sales["quantity"], errors="coerce")
sales["unit_price"] = pd.to_numeric(sales["unit_price"], errors="coerce")
sales["sales"] = sales["quantity"] * sales["unit_price"]

sales_by_region = pd.pivot_table(
    sales,
    values="sales",
    index="sales_region",
    columns="order_type",
    aggfunc=np.sum,
    margins=True,
    margins_name="Total",
)

pd.set_option("display.max_columns", None)
print("Sales by region and order type:")
print(sales_by_region)