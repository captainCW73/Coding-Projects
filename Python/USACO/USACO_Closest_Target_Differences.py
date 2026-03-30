info = list(map(int, input().split()))
target = info[0]
remaining = info[1:]
differences = []
count = 0

while remaining:
    closest = remaining[0]
    for i in remaining:
        if abs(i - target) < abs(closest - target):
            closest = i
    count += 1
    if count != 2 and count != 4:
        differences.append(abs(target - closest))
    target = closest
    remaining.remove(closest)

print(sum(differences))
