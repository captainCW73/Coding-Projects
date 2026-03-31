first_input = input().split()
n = int(first_input[0])
intervals = []
for _ in range(n):
    lifeguards_line = input("").split()
    start, end = int(lifeguards_line[0]), int(lifeguards_line[1])
    intervals.append((start, end))

for start, end in intervals:
    string_list = [str(f) for f in range(start + 1, end)]

