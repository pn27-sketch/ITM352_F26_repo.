emotions = ("happy", "sad", "fear", "surprise")
condition = emotions[-1] == "happy" and len(emotions) > 3
print(("false", "true")[condition])