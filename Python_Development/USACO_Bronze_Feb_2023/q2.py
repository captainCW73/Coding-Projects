import sys
input = sys.stdin.readline
t = int(input())

DIGIT_MAP = {'0':'0','1':'1','2':'0','3':'1','4':'0','5':'1','6':'0','7':'1','8':'0','9':'1'}

def process(n):
    s = list(str(n))
    changed = False
    for i in range(len(s)):
        if s[i] not in {'0', '1'}:
            s[i] = DIGIT_MAP[s[i]]
            changed = True
    return int(''.join(s)), changed

strings = []
for i in range(t):
    x = input().strip()
    strings.append(x)

out = []
for x in strings:
    n = int(x)
    count = 0
    while n != 0:
        n, changed = process(n)
        if changed:
            count += 1
        else:
            n -= 1
            count += 1
    out.append(str(count))

sys.stdout.write('\n'.join(out) + '\n')