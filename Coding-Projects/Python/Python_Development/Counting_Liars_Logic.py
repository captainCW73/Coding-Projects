import sys
input = sys.stdin.readline
n = int(input())
cows = []
possible_liars = 0
for _ in range(n):
    line = input().strip().split()
    cows.append((line[0], line[1],))
ans = n
for _, pos in cows:
    side = _
    liars = 0
    for j, p in cows:
        if side == 'G' and p < pos:
            liars += 1
        elif side == 'L' and p > pos:
            liars += 1
    if liars < ans:
        ans = liars
print(ans)