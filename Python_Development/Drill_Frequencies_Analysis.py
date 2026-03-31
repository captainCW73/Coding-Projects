word_numbers = int(input(""))
counts = {}
for _ in range(word_numbers):
    word = input("")
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1
for word in counts:
    print(f"{word} {counts[word]}")
