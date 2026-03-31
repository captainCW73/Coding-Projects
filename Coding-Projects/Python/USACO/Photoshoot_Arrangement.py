nkint = (input("")).split()
n = int(nkint[0])
k = int(nkint[1])
q = int(input(""))
max_acttractiveness = 0
cow_values = [[0] * (n + 1) for _ in range(n + 1)]
square_sums = [[0] * (n + 1) for _ in range(n + 1)]
final_print = ""
for _ in range(q):
    rcv = input("").split()
    r = int(rcv[0])
    c = int(rcv[1])
    v = int(rcv[2])
    diff = v - cow_values[r][c]
    cow_values[r][c] = v
    r_start = max(1, r - k + 1)
    r_end = min(n - k + 1, r)
    c_start = max(1, c - k + 1)
    c_end = min(n - k + 1, c)
    for i in range(r_start, r_end + 1):
        for j in range(c_start, c_end + 1):
            square_sums[i][j] += diff
            if square_sums[i][j] > max_acttractiveness:
                max_acttractiveness = square_sums[i][j]
    final_print += str(max_acttractiveness) + "\n"
print(final_print, end="")
    