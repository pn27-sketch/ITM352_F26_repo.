# Hypothesis: each loop iteration replaces the running total instead of adding to it.
prices = [5.95, 3.00, 12.50]
total_price = 0
tax_rate = 1.08  # 8% tax multiplier

for price in prices:
    total_price += price * tax_rate

print(f"Total price (with tax): ${total_price:.2f}")