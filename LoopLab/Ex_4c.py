import unittest

from LoopLab.Ex_4a import check_budget


class CheckBudgetTests(unittest.TestCase):
	def test_purchase_over_budget(self):
		self.assertEqual(check_budget(60.00, 50.00), "This purchase is over budget!")

	def test_purchase_within_budget(self):
		self.assertEqual(check_budget(40.00, 50.00), "This purchase is within budget")

	def test_purchase_equal_to_budget_is_within_budget(self):
		self.assertEqual(check_budget(50.00, 50.00), "This purchase is within budget")


if __name__ == "__main__":
	unittest.main()