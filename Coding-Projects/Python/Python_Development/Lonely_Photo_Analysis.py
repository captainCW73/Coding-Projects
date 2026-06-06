import sys
input = sys.stdin.readline

n = int(input())
cows = input().strip()

total_lonely = 0

for start in range(len(cows)):
    g_count = 0
    h_count = 0
    
    for end in range(start, len(cows)):
        if cows[end] == 'G':
            g_count += 1
        else:
            h_count += 1
            
        if (end - start + 1) >= 3:
            if g_count == 1 or h_count == 1:
                total_lonely += 1
            elif g_count > 1 and h_count > 1:
                break

print(total_lonely)