import sys
input = sys.stdin.readline

nm = input().split()
n = int(nm[0])
m_limit = int(nm[1])

for i in range(n):
    stc = input().split()
    s = int(stc[0])
    t = int(stc[1])
    c = int(stc[2])
    print(t)

for i in range(m_limit):
    abpm = input().split()
    a = int(abpm[0])
    b = int(abpm[1])
    p = int(abpm[2])
    m = int(abpm[3])
