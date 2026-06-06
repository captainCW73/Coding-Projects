import sys
input = sys.stdin.readline

last_g = 0
last_h = 0

t_str = input().strip()
t = int(t_str)
for _ in range(t):
    line = input().split()
    if len(line) == 2:
        n, k = map(int, line)
    cows = list(input().strip())
    satisfied = 0
    for i in range(n):
        if cows[i] == '1':
            satisfied += 1
        else:
            left = max(0, i - k)
            right = min(n - 1, i + k)
            if '1' not in cows[left:right + 1]:
                cows[i] = '1'
                satisfied += 1
    for _ in range(k):


    