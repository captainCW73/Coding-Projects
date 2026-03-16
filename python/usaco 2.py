n = int(input()) #of tries
all_trials = []

for i in range(n):
    trial = list(map(int, input().split()))
    all_trials.append(trial)


all_max_counts = []
for position in range(3):
    counts = {}
    for num in position_numbers:
        counts[num] = counts.get(num, 0) + 1
    
    # Get the maximum count for this position
    max_count = max(counts.values())
    all_max_counts.append(max_count)


final_count = max(all_max_counts)
print(final_count)