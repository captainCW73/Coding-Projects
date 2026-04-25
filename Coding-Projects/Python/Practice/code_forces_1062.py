num_cases = int(input().strip())

# 1) Read and store all test cases
all_cases = []
for _ in range(num_cases):
    sticks = list(map(int, input().split()))
    all_cases.append(sticks)

# 2) Process and print AFTER all input is done
for sticks in (all_cases):
    sticks.sort()
    if len(sticks) >= 4 and sticks[0] == sticks[1] == sticks[2] == sticks[3]:
        print("YES")
    else:
        print("NO")
