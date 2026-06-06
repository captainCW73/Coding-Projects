import sys
input = sys.stdin.readline

def solve():
    N, K = map(int, input().split())
    a = list(map(int, input().split()))
    absK = abs(K)
    groups = {}
    for x in a:
        r = x % absK
        if r not in groups:
            groups[r] = []
        groups[r].append(x)
    ElsieNumber = 0
    for vals in groups.values():
        vals.sort(reverse=K < 0)
        prev = None
        for orig in vals:
            assigned = orig if prev is None else (min if K < 0 else max)(orig, prev + K)
            ElsieNumber += abs(assigned - orig) // absK
            prev = assigned
    print(ElsieNumber)

T = int(input())
for _ in range(T):
    solve()