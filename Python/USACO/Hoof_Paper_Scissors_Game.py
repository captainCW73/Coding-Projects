import sys
input = sys.stdin.readline
print = sys.stdout.write
n = int(input())
max_wins = 0
count = 0
for i in range(n):
    games = input().split()
    cow_1 = int(games[0])
    cow_2 = int(games[1])
    if cow_1 != cow_2:
        if (cow_1 == 0 and cow_2 == 2) or (cow_1 == 1 and cow_2 == 0) or (cow_1 == 2 and cow_2 == 1):
            count += 1
        if (cow_1 == 1 and cow_2 == 3) or (cow_1 == 2 and cow_2 == 0) or (cow_1 == 3 and cow_2 == 1):
            count += 1
ans = max(max_wins, count)
print(str(ans) + "\n")