from sys import stdin, stdout
input = stdin.readline
output = stdout.write
n = list(map(int, input().split()))
n.sort()
a_b_c = max(n)
a = n[0]
b = n[1]
c = a_b_c - a - b
if a_b_c >= a + b:
    print(a, b, c)