from pathlib import Path

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

print("Sales data loaded successfully.")
print(f"Rows and columns: {sales.shape}")
print("\nData types:")
print(sales.dtypes)

print("\nFirst 10 rows with order_date in standard date format:")
print(sales.head(10).to_string(index=False))