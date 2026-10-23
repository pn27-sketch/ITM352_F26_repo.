# Hypothesis: range(10) starts at 0 and excludes 10, and continue on other
# numbers skips the later break condition, so the loop never stops at 8.
for x in range(1, 11):
    if x == 5:
        continue
    if x == 8:
        print("done!")
        break
    print(x)