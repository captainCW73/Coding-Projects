import sys
input = sys.stdin.readline
print = sys.stdout.write

n = int(input())
cows = list(map(int, input().split()))
stalls = list(map(int, input().split()))

cows.sort(reverse=True)
stalls.sort(reverse=True)

ans = 1
for i in range(n):
    fits = 0
    for s in stalls:
        if s >= cows[i]:
            fits += 1
    ans *= (fits - i)

print(str(ans) + '\n')