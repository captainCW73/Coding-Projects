cowtab = input("").split()
num = list(map(int, cowtab))
mildred = 0
elsie = 0
bessie = 0
mildred_increases = 0
elsie_increases = 0
bessie_increases = 0
display_counter = 0
entries = []
for _ in range(num[0]):
    num_line = input().split()
    # num_line structure assumed: [number, name, ...]
    day = int(num_line[0])
    name = num_line[1]
    # collect any other details you want to keep
    other_fields = num_line[2:]
    entries.append((day, name, *other_fields))

# Sort entries by 'day' (the first element in tuple)
entries.sort()
for entry in entries:
    if entry[1] == "Mildred":
        mildred += int(entry[2])    
        mildred_increases += 1
    elif entry[1] == "Elsie":
        elsie += int(entry[2])
        elsie_increases += 1
    elif entry[1] == "Bessie":
        bessie += int(entry[2])
        bessie_increases += 1
    if mildred == elsie == bessie:
        current_counts = {'Mildred': mildred, 'Elsie': elsie, 'Bessie': bessie}
        max_count = max(current_counts.values())
        cows_with_max = [cow for cow, count in current_counts.items() if count == max_count]
        if len(cows_with_max) == 1:
            display_counter += 1
ordered_cows = sorted([mildred, elsie, bessie])
print(mildred_increases + elsie_increases + bessie_increases)
