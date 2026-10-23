# Hypothesis: removing items while iterating shifts later scores past the loop.
scores = [60, 45, 30, 85, 10, 90]

scores = [score for score in scores if score >= 50]
print(scores)