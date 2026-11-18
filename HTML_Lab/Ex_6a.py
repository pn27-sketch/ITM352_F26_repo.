import requests
from bs4 import BeautifulSoup


URL = "https://www.hicentral.com/hawaii-mortgage-rates.php"

response = requests.get(URL, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
rate_table = soup.find("table")
if rate_table is None:
    raise ValueError("Could not find the mortgage rate table.")

current_bank = None
rows = rate_table.find_all("tr")
for row in rows[1:]:
    cells = row.find_all("td")
    lender_cell = row.find("td", rowspan=True)
    if lender_cell is not None:
        bank_name = lender_cell.find("b")
        if bank_name is None:
            raise ValueError("Could not find a bank name in the rate table.")
        current_bank = bank_name.get_text(" ", strip=True)
        rate_cells = cells[1:]
    else:
        rate_cells = cells

    values = [cell.get_text(" ", strip=True) for cell in rate_cells]
    values.extend([""] * (4 - len(values)))
    term, interest_rate, points, apr = values[:4]

    print(
        f"{current_bank} | {term}: "
        f"Interest rate: {interest_rate or 'Not listed'}%; "
        f"Points: {points or 'Not listed'}%; "
        f"APR: {apr or 'Not listed'}%"
    )