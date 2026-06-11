some_list = ['a', 'b', 'c', 'b', 'd', 'm', 'n', 'n']
non_dupes = []
dupes = []
for item in some_list:
    if item not in non_dupes:
        non_dupes.append(item)
    else:
        dupes.append(item)
print(dupes)