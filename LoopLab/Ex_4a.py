recent_purchases = [36.13, 23.87, 183.35, 22.93, 11.62]
budget = 50.00


def check_budget(expense, budget):
	if expense > budget:
		return "This purchase is over budget!"
	return "This purchase is within budget"


if __name__ == "__main__":
	for expense in recent_purchases:
		print(check_budget(expense, budget))