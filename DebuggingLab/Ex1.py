# Hypothesis: the price is stored as currency text, so multiplying it by the tax rate will fail.

from typing import TypedDict


class Product(TypedDict):
    name: str
    price: float


def calculate_total(price: float, tax_rate: float) -> float:
    return price * (1 + tax_rate)


product: Product = {
    "name": "small gumball",
    "price": 0.34,
}
tax_rate = 0.045

total = calculate_total(product["price"], tax_rate)
print(f"A {product['name']} costs ${total:.2f}")