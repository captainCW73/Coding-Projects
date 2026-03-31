tk_input = input("").split()
t = int(tk_input[0])
k = int(tk_input[1])
square = False
results = []
for _ in range(t):
    n = int(input(""))
    s = input("")
    count = 0
    if n%2 != 0:
        results.append("-1")
        continue
    middle = 3*n//2
    first_half = s[:middle]
    second_half = s[middle:]
    if first_half == second_half:
        results.append("1")
        continue
    else:
        results.append("2")
        res = (["1"] * middle) +(["2"] * middle)
        results.append(" ".join(res))
print("\n".join(results))