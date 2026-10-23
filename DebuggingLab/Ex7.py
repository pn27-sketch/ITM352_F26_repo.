# Hypothesis: the running total carries across people, and the Gold boundary
# check excludes an average of exactly 10,000 steps.
weekly_steps = {
    "Kai": [8000, 9500, 7200, 11000, 6800, 12000, 9000],
    "Leilani": [12000, 9000, 10500, 8500, 11000, 9500, 9500],
    "Noa": [4000, 5200, 3800, 6100, 4500, 5000, 4400],
}


def choose_badge(average):
    if average >= 10000:
        return "Gold"
    elif average >= 7500:
        return "Silver"
    else:
        return "Bronze"


for name, days in weekly_steps.items():
    total = 0
    for steps in days:
        total += steps
    average = total / len(days)
    badge = choose_badge(average)
    print(name.ljust(8), "average:", format(average, ",.0f"), "steps/day ->", badge)