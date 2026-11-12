import sys
import time

import pandas as pd

# Dashboard settings.
data_file = "sales_data.csv"
column_renames = {"produce_name": "product_name"}
numeric_columns = ["quantity", "unit_price", "sales"]
allowed_aggregations = ["sum", "mean", "count", "min", "max", "nunique"]
pivot_row_fields = ["employee_name", "job_title", "sales_region", "customer_state",
                    "customer_name", "customer_type", "order_type",
                    "product_category", "product_name", "year", "quarter"]
pivot_column_fields = ["order_type", "customer_type", "product_category",
                       "sales_region", "year", "quarter"]
pivot_value_fields = ["quantity", "unit_price", "sales"]
pivot_aggregations = ["sum", "mean", "count", "min", "max"]

max_rows_shown = 40
max_columns_before_warning = 20

derived_from = {
    "sales": "quantity and unit_price",
    "year": "order_date",
    "month": "order_date",
    "quarter": "order_date",
}

# This function loads the CSV file and returns the DataFrame.
def load_data(filename):
    while True:
        start_time = time.perf_counter()
        print(f"Loading sales data from '{filename}'...")
        try:
            df = pd.read_csv(filename)
            elapsed = time.perf_counter() - start_time
            if df.empty:
                print(f"Load status: failed - the file '{filename}' has no data rows.")
                return None

            print("Load status: success")
            print(f"Load time: {elapsed:.2f} seconds")
            print(f"Rows loaded: {len(df):,}")
            print(f"Available columns: {', '.join(df.columns.astype(str).tolist())}")
            return df
        except FileNotFoundError:
            print(f"Load status: failed - could not find the file '{filename}'.")
        except PermissionError:
            print(f"Load status: failed - no permission to open '{filename}'. Is it open in another program?")
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            print(f"Load status: failed - '{filename}' is empty or not a valid CSV file.")
            return None

        filename = input("Type the file name/path to try again (or press Enter to quit): ").strip()
        if filename == "":
            return None


# This function standardizes the column names and fixes known naming issues.
def normalize_columns(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    for old_name, new_name in column_renames.items():
        if old_name in df.columns and new_name not in df.columns:
            df = df.rename(columns={old_name: new_name})
    return df


# This function creates year, month, and quarter fields from the order date.
def add_date_parts(df):
    if "order_date" not in df.columns:
        return 0

    dates = pd.to_datetime(df["order_date"].astype(str), dayfirst=True,
                           format="mixed", errors="coerce")
    bad_dates = int(dates.isna().sum())
    df["year"] = dates.dt.year.fillna(0).astype(int)
    df["month"] = dates.dt.month.fillna(0).astype(int)
    df["quarter"] = dates.dt.quarter.fillna(0).astype(int)
    return bad_dates


# This function fills missing values with zeros while keeping text columns usable.
def fill_missing_values(df):
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna("0").astype(str)
    return int(df.isna().sum().sum())


# This function cleans the dataset before analysis by fixing names, values, and dates.
def clean_data(df):
    df = normalize_columns(df)

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"].astype(str), dayfirst=True,
                                          format="mixed", errors="coerce")

    bad_dates = add_date_parts(df)
    missing_count = fill_missing_values(df)

    if missing_count == 0 and bad_dates == 0:
        print("Data check: no missing values found.")
    if missing_count > 0:
        print(f"Data check: {missing_count} missing/invalid values were replaced with 0.")
    if bad_dates > 0:
        print(f"Data check: {bad_dates} order dates could not be read; their year/month/quarter were set to 0.")

    if "sales" not in df.columns and {"quantity", "unit_price"} <= set(df.columns):
        df["sales"] = df["quantity"] * df["unit_price"]

    # Explicit casting helps guard against dtype drift and keeps the analytics stable.
    for col in ["quantity", "unit_price", "sales"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


# This function returns the columns that are still missing from the DataFrame.
def find_missing_columns(df, needed):
    return [col for col in needed if col not in df.columns]


# This function turns missing-column information into a readable message.
def describe_missing(missing):
    return ", ".join(
        f"{col} (calculated from {derived_from[col]}, so those are needed)"
        if col in derived_from else col
        for col in missing
    )


# This function checks which required fields are missing for a chosen dashboard option.
def missing_required_columns(df, function):
    return find_missing_columns(df, required_columns.get(function, []))


# This function adds a total row and, when needed, a total column to a table.
def add_totals(table, has_columns):
    if has_columns:
        table["Total"] = table.sum(axis=1)
    table.loc["Total"] = table.sum()
    return table


# This function creates a one-way summary table grouped by one field.
def one_way_table(df, row_col, top=None):
    table = pd.pivot_table(df, index=row_col, values=["quantity", "sales"],
                           aggfunc="sum")[["quantity", "sales"]]
    table = table.sort_values("sales", ascending=False)
    if top is not None:
        return table.head(top)
    table = add_totals(table, has_columns=False)
    table["quantity"] = table["quantity"].astype(int)
    return table


# This function creates a two-way summary table for total sales across two groups.
def two_way_table(df, row_col, col_col, sort=True):
    table = pd.pivot_table(df, index=row_col, columns=col_col,
                           values="sales", aggfunc="sum")
    column_means = table.mean()
    table["Total"] = table.sum(axis=1)
    if sort:
        table = table.sort_values("Total", ascending=False)
    table.loc["Total"] = table.sum()
    return table.fillna(column_means)


# This function appends a total row to a DataFrame with multi-level indexes.
def add_grand_total(table):
    if table.index.nlevels == 1:
        table.loc["Total"] = table.sum()
        return table
    label = ("Total",) + ("",) * (table.index.nlevels - 1)
    total_row = pd.DataFrame(
        [table.sum()],
        index=pd.MultiIndex.from_tuples([label], names=table.index.names))
    return pd.concat([table, total_row])


# This function shows average sales by region and state, split by order type.
def region_state_average_table(df):
    by_state = pd.pivot_table(df, index=["sales_region", "customer_state"],
                              columns="order_type", values="sales",
                              aggfunc="mean", margins=True, margins_name="All")
    by_state = by_state.drop("All", level=0)
    by_state = by_state.fillna(by_state.mean())

    by_region = pd.pivot_table(df, index="sales_region", columns="order_type",
                               values="sales", aggfunc="mean",
                               margins=True, margins_name="All")
    by_region.index = pd.MultiIndex.from_tuples(
        [(region, "(all states)") for region in by_region.index],
        names=by_state.index.names)
    grand_row = by_region.loc[["All"]]
    grand_row.index = pd.MultiIndex.from_tuples([("All regions", "")],
                                                names=by_state.index.names)
    by_region = by_region.drop("All", level=0)
    by_region = by_region.fillna(by_region.mean())

    table = pd.concat([by_state, by_region]).sort_index()
    return pd.concat([table, grand_row])


# This function shows sales totals by state and customer/order type.
def state_type_table(df):
    table = pd.pivot_table(df, index=["customer_state", "customer_type", "order_type"],
                           values="sales", aggfunc="sum")
    return add_grand_total(table)


# This function summarizes quantity and sales totals for selected groupings.
def quantity_sales_table(df, index_columns):
    table = pd.pivot_table(df, index=index_columns, values=["quantity", "sales"],
                           aggfunc="sum")[["quantity", "sales"]]
    table = add_grand_total(table)
    table["quantity"] = table["quantity"].astype(int)
    return table


# This function shows total sales and the price range in each product category.
def price_range_table(df):
    table = pd.pivot_table(df, index="product_category",
                           values=["sales", "unit_price"],
                           aggfunc={"sales": "sum", "unit_price": ["max", "min"]})
    table.columns = ["_".join(column) for column in table.columns]
    table = table.rename(columns={"sales_sum": "total_sales",
                                  "unit_price_max": "max_price",
                                  "unit_price_min": "min_price"})
    table = table[["total_sales", "max_price", "min_price"]]
    return table.sort_values("total_sales", ascending=False)


# This function normalizes a value so it behaves like a list.
def as_list(item):
    if item is None:
        return []
    if isinstance(item, str):
        return [item]
    return list(item)


# This function builds the pivot table selected by the user.
def build_custom_pivot(df, rows, values, aggfuncs, columns=None):
    rows, values = as_list(rows), as_list(values)
    aggfuncs, columns = as_list(aggfuncs), as_list(columns)

    if df.empty:
        raise ValueError("There is no data to analyse.")
    if not rows:
        raise ValueError("Choose at least one row field.")
    if not values:
        raise ValueError("Choose at least one values field.")
    if not aggfuncs:
        raise ValueError("Choose at least one aggregation function.")
    for col in rows + columns + values:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' does not exist.")
    for col in values:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column '{col}' is not numeric, so it cannot be summarised.")
    for func in aggfuncs:
        if func not in allowed_aggregations:
            raise ValueError(f"'{func}' is not one of {allowed_aggregations}.")
    all_fields = rows + columns + values
    if len(set(all_fields)) != len(all_fields):
        raise ValueError("Each field can only be used once (rows, columns and values must all be different).")

    table = pd.pivot_table(df, index=rows, columns=columns or None,
                           values=values[0] if len(values) == 1 else values,
                           aggfunc=aggfuncs[0] if len(aggfuncs) == 1 else aggfuncs)
    column_means = table.mean()

    if len(aggfuncs) == 1 and aggfuncs[0] in ("sum", "count"):
        if columns and len(values) == 1:
            table["Total"] = table.sum(axis=1)
        table = add_grand_total(table)

    return table.fillna(column_means)


# This function converts text like "1, 3" into a list of valid numbers.
def parse_numbers(text, maximum):
    numbers = []
    for part in text.split(","):
        part = part.strip()
        if not part.isdigit():
            return None
        number = int(part)
        if number < 1 or number > maximum:
            return None
        if number not in numbers:
            numbers.append(number)
    return numbers


# This function asks the user to choose one or more numbered menu options.
def ask_choices(title, options, optional=False, single=False):
    while True:
        print(f"\n{title}")
        for number, option in enumerate(options, start=1):
            print(f"{number}. {option}")
        if single:
            prompt = "Enter the number of your choice: "
        elif optional:
            prompt = "Enter the number(s) of your choice(s), separated by commas (enter for no grouping): "
        else:
            prompt = "Enter the number(s) of your choice(s), separated by commas: "
        answer = input(prompt).strip()

        if answer == "" and optional:
            return []
        numbers = parse_numbers(answer, len(options))
        if numbers is not None and single and len(numbers) != 1:
            numbers = None
        if numbers is None:
            if single:
                print(f"Invalid input. Please type one number from 1 to {len(options)}.")
            else:
                print(f"Invalid input. Please type numbers from 1 to {len(options)}, separated by commas (for example: 1,2).")
            continue
        return [options[number - 1] for number in numbers]


# This function asks a yes-or-no question and returns a boolean value.
def ask_yes_no(question):
    return input(question + " (y/n): ").strip().lower() == "y"


# This function asks how many rows the user wants to preview.
def ask_row_count(total_rows):
    print(f"\nThe sales data has {total_rows} rows available.")
    while True:
        print("\nEnter rows to display:")
        print(f"- Enter a number 1 to {total_rows}")
        print("- To see all rows, enter 'all'")
        print("- To skip preview, press Enter")
        answer = input("Your choice: ").strip().lower()

        if answer == "":
            return 0
        if answer == "all":
            return total_rows
        if answer.isdigit() and 1 <= int(answer) <= total_rows:
            return int(answer)
        print(f"Invalid input. Please enter a number from 1 to {total_rows}, 'all', or press Enter.")


# This function offers the user the option to save the table as a CSV file.
def offer_save(table):
    if not ask_yes_no("Save this table to a CSV file?"):
        return
    filename = input("File name (for example result.csv): ").strip()
    if filename == "":
        print("No name given, so nothing was saved.")
        return
    if not filename.lower().endswith(".csv"):
        filename += ".csv"
    try:
        table.to_csv(filename)
        print(f"Saved to '{filename}'.")
    except OSError as error:
        print(f"Could not save the file: {error}")


# This function displays a table with a title and offers to save it.
def show_table(title, table):
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70)
    if table.empty:
        print("No data to show.")
        return
    print(table)
    if len(table) > max_rows_shown:
        print(f"\n(The table has {len(table)} rows, so the middle is hidden. Save it to a CSV file to see everything.)")
    offer_save(table)


# This function converts a table into text lines for display in the terminal.
def table_to_lines(title, table):
    text = table.to_string(max_rows=max_rows_shown,
                           float_format="{:,.2f}".format)
    return [title, "-" * len(title)] + text.split("\n")


# This function places two text blocks side by side so they can be compared.
def join_side_by_side(left_lines, right_lines, separator="   |   "):
    left_width = max(len(line) for line in left_lines)
    height = max(len(left_lines), len(right_lines))
    left_lines = left_lines + [""] * (height - len(left_lines))
    right_lines = right_lines + [""] * (height - len(right_lines))
    joined = [left.ljust(left_width) + separator + right
              for left, right in zip(left_lines, right_lines)]
    return "\n".join(joined)


# This function prints two tables next to each other for side-by-side comparison.
def show_side_by_side(left_title, left_table, right_title, right_table):
    text = join_side_by_side(table_to_lines(left_title, left_table),
                             table_to_lines(right_title, right_table))
    widest = max(len(line) for line in text.split("\n"))
    print("\n" + "=" * min(widest, 200))
    print(text)
    print("=" * min(widest, 200))

# This function keeps only the fields that exist in the DataFrame.
def available_fields(df, wanted_fields):
    return [field for field in wanted_fields if field in df.columns]

# This function creates a valid list of options, optionally filtering to numeric fields.
def available_field_options(df, wanted_fields, *, numeric_only=False, exclude=None):
    exclude = set(exclude or [])
    options = []
    for field in available_fields(df, wanted_fields):
        if field in exclude:
            continue
        if numeric_only and not pd.api.types.is_numeric_dtype(df[field]):
            continue
        options.append(field)
    return options


# This function asks the user to choose the pivot table rows, columns, values, and aggregation.
def ask_pivot_settings(df):
    row_options = available_fields(df, pivot_row_fields)
    value_options = available_field_options(df, pivot_value_fields, numeric_only=True)
    if not row_options or not value_options:
        print("The data does not have the fields needed for the pivot table generator (at least one grouping field and one numeric field).")
        return None

    rows = ask_choices("Select rows:", row_options)
    column_options = available_field_options(df, pivot_column_fields, exclude=rows)
    columns = []
    if column_options:
        columns = ask_choices("Select columns (optional):", column_options, optional=True)
    else:
        print("\nNo fields are left for columns, so there is no column grouping.")

    values = ask_choices("Select values:", value_options)
    aggfuncs = ask_choices("Select aggregation function:", pivot_aggregations)
    return rows, columns, values, aggfuncs


# This function checks whether the pivot table would be too wide and asks before continuing.
def warn_if_pivot_is_wide(df, columns):
    if not columns:
        return False

    wide_count = len(df[columns].drop_duplicates())
    if wide_count <= max_columns_before_warning:
        return False

    print(f"Warning: your column choice gives {wide_count} different column groups, so the table would be very wide.")
    return not ask_yes_no("Continue anyway?")


# This function builds a custom pivot table based on the user's selections.
def custom_pivot(df):
    print("\n--- PIVOT TABLE GENERATOR ---")
    settings = ask_pivot_settings(df)
    if settings is None:
        return None

    rows, columns, values, aggfuncs = settings
    if warn_if_pivot_is_wide(df, columns):
        return None

    try:
        table = build_custom_pivot(df, rows, values, aggfuncs, columns)
    except ValueError as error:
        print(f"Could not build the pivot table: {error}")
        return None
    except Exception as error:
        print(f"Something went wrong: {error}")
        return None

    title = f"{', '.join(aggfuncs)} of {', '.join(values)} by {', '.join(rows)}"
    if columns:
        title += f" and {', '.join(columns)}"
    table.attrs["title"] = title
    return table


# This function shows the first rows of the dataset based on the user's choice.
def show_first_rows(df):
    count = ask_row_count(len(df))
    if count == 0:
        print("Preview skipped.")
        return None
    print(f"\nFirst {count} of {len(df)} rows of sales data:")
    with pd.option_context("display.max_rows", None):
        print(df.head(count))
    return None


# This function shows total sales by region and order type.
def sales_by_region_and_order_type(df):
    return two_way_table(df, "sales_region", "order_type")


# This function shows average sales by region and state.
def average_sales(df):
    return region_state_average_table(df)


# This function shows sales by state and customer/order type.
def sales_by_types_and_state(df):
    return state_type_table(df)


# This function shows quantity and sales totals by region and product.
def quantity_price_by_region_product(df):
    return quantity_sales_table(df, ["sales_region", "product_name"])


# This function shows quantity and sales totals by order type and customer type.
def quantity_price_by_order_and_customer_type(df):
    return quantity_sales_table(df, ["order_type", "customer_type"])


# This function shows product category sales and the price range within each category.
def max_min_price_by_category(df):
    return price_range_table(df)


# This function counts the unique employees working in each region.
def unique_employees_by_region(df):
    table = build_custom_pivot(df, "sales_region", "employee_id", "nunique")
    table.columns = ["unique_employees"]
    return table


# This function creates the list of menu items and checks which required fields are missing.
def menu_items_for_df(df, *, comparable_only=False):
    for item in menu_items:
        text, function = unpack_item(item)
        if comparable_only and function in not_comparable:
            continue

        missing = missing_required_columns(df, function)
        if comparable_only and missing:
            continue

        yield text, function, missing


# This function lets the user compare two dashboard analytics side by side.
def compare_analytics(df):
    choices = [(text, function) for text, function, _ in menu_items_for_df(df, comparable_only=True)]
    if not choices:
        print("No analytics are available to compare with this data.")
        return None

    names = [text for text, function in choices]
    print("\n--- COMPARE TWO ANALYTICS ---")
    results = []
    for label in ("FIRST", "SECOND"):
        picked = ask_choices(f"Select the {label} analytic:", names, single=True)[0]
        text, function = choices[names.index(picked)]
        table = run_analytic(df, text, function)
        if not isinstance(table, pd.DataFrame):
            print(f"The {label.lower()} analytic did not give a table, so there is nothing to compare.")
            return None
        results.append((table.attrs.get("title", text), table))

    (left_title, left_table), (right_title, right_table) = results
    show_side_by_side(left_title, left_table, right_title, right_table)
    return None


# This function exits the dashboard and tells the menu loop to stop.
def exit_program(df):
    print("Goodbye!")
    return True


# Required columns for each dashboard option.
required_columns = {
    sales_by_region_and_order_type: ["sales_region", "order_type", "sales"],
    average_sales: ["sales_region", "customer_state", "order_type", "sales"],
    sales_by_types_and_state: ["customer_state", "customer_type",
                               "order_type", "sales"],
    quantity_price_by_region_product: ["sales_region", "product_name",
                                       "quantity", "sales"],
    quantity_price_by_order_and_customer_type: ["order_type", "customer_type",
                                                "quantity", "sales"],
    max_min_price_by_category: ["product_category", "sales", "unit_price"],
    unique_employees_by_region: ["sales_region", "employee_id"],
}


# This tuple defines the menu items shown to the user.
menu_items = (
    {"Show the first n rows of sales data": show_first_rows},
    {"Total sales by region and order_type": sales_by_region_and_order_type},
    {"Average sales by region with average sales by state and sale type": average_sales},
    {"Sales by customer type and order type by state": sales_by_types_and_state},
    {"Total sales quantity and price by region and product": quantity_price_by_region_product},
    {"Total sales quantity and price by order type and customer type": quantity_price_by_order_and_customer_type},
    {"Max and min sales price of sales by category": max_min_price_by_category},
    {"Number of unique employees by region": unique_employees_by_region},
    {"Create a custom pivot table": custom_pivot},
    {"Compare two analytics side by side": compare_analytics},
    {"Exit": exit_program},
)


# Menu items that cannot be compared side by side.
not_comparable = (show_first_rows, compare_analytics, exit_program)


# This function extracts a label and function from a menu item dictionary.
def unpack_item(item):
    return next(iter(item.items()))


# This function checks that every menu entry is valid and callable.
def check_menu():
    is_ok = True
    for position, item in enumerate(menu_items, start=1):
        if not isinstance(item, dict) or len(item) != 1:
            print(f"Menu setup problem: item {position} must be a dictionary with exactly one entry.")
            is_ok = False
        elif not callable(unpack_item(item)[1]):
            print(f"Menu setup problem: item {position} has no function.")
            is_ok = False
    return is_ok


# This function checks the data for missing columns and prints a warning when needed.
def show_data_check(df):
    print("\n--- FIELD CHECK ---")
    missing_items = [(text, missing) for text, _, missing in menu_items_for_df(df) if missing]
    if not missing_items:
        print("All required fields were found. Every menu item is available.")
        return

    print("WARNING: some fields needed by the dashboard are missing from your data.")
    print("These menu items may not work:")
    for text, missing in missing_items:
        print(f"  - {text}: missing {describe_missing(missing)}")
    print("The custom pivot table still works with the columns you do have.")


# This function prints the menu and marks options that are unavailable for the current data.
def show_menu(df):
    print("\n" + "=" * 70 + "\nSALES DASHBOARD\n" + "=" * 70)
    for number, (text, _, missing) in enumerate(menu_items_for_df(df), start=1):
        note = "  [UNAVAILABLE - missing fields]" if missing else ""
        print(f"  {number}. {text}{note}")


# This function safely runs a dashboard action and returns the result or a failure message.
def run_analytic(df, text, function):
    missing = missing_required_columns(df, function)
    if missing:
        print(f"\nSorry, '{text}' cannot run because these fields are missing: {describe_missing(missing)}.")
        return None
    try:
        return function(df)
    except Exception as error:
        print(f"Something went wrong while running '{text}': {error}")
        return None


# This function executes the selected menu option and shows the resulting table.
def run_menu_item(df, number):
    text, function = unpack_item(menu_items[number - 1])
    result = run_analytic(df, text, function)
    if result is True:
        return True
    if isinstance(result, pd.DataFrame):
        show_table(result.attrs.get("title", text), result)
    return False


# This function runs a focused set of assertions against sample data to verify the dashboard logic.
def run_self_tests():
    test_df = pd.DataFrame({
        "employee_name": ["Alice", "Bob", "Alice"],
        "sales_region": ["North", "North", "South"],
        "customer_state": ["CA", "WA", "CA"],
        "customer_type": ["Retail", "Retail", "Wholesale"],
        "order_type": ["Online", "InStore", "Online"],
        "product_category": ["Electronics", "Electronics", "Home"],
        "product_name": ["Laptop", "Laptop", "Lamp"],
        "quantity": [2, 1, 3],
        "unit_price": [1000, 700, 50],
        "sales": [2000, 700, 150],
        "order_date": ["2024-01-02", "2024-04-05", "2024-07-15"],
    })

    cleaned = clean_data(test_df)
    assert set(["year", "month", "quarter"]).issubset(cleaned.columns)
    assert cleaned["quantity"].dtype.kind in "iuf"
    assert cleaned["unit_price"].dtype.kind in "iuf"
    assert cleaned["sales"].dtype.kind in "iuf"
    assert cleaned["sales"].sum() == 2850.0

    pivot = build_custom_pivot(cleaned, ["sales_region"], ["sales"], ["sum"])
    assert float(pivot.loc["Total", "sales"]) == 2850.0

    avg = average_sales(cleaned)
    assert isinstance(avg, pd.DataFrame)
    assert not avg.empty

    print("Self-test passed: dashboard calculations and required fields validated.")


# This function runs the main dashboard loop from start to finish.
def main():
    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", 30)
    pd.set_option("display.max_rows", max_rows_shown)
    pd.set_option("display.float_format", "{:,.2f}".format)

    if "--test" in sys.argv:
        run_self_tests()
        return

    print("Welcome to the Sales Dashboard!\n")
    if not check_menu():
        return
    df = load_data(data_file)
    if df is None:
        print("No data was loaded, so the dashboard cannot start. Goodbye!")
        return

    df = clean_data(df)
    show_data_check(df)

    try:
        while True:
            show_menu(df)
            choice = input(f"\nChoose an option (1-{len(menu_items)}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(menu_items):
                if run_menu_item(df, int(choice)):
                    break
            else:
                print("That is not a valid option. Please type a number from the menu.")
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")


# This guard ensures the dashboard runs only when the file is run directly.
if __name__ == "__main__":
    main()