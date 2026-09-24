sentence = input("Enter a sentence: ")
words = sentence.split()
words.reverse()
reversed_sentence = " ".join(words)

print(reversed_sentence)