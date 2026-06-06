from sys import stdin, stdout
input = stdin.readline
output = stdout.write
n = int(input())
for i in range(n):
    cows = input().strip()
    parts = cows.split()
    names = parts[0::2]
    milk_amount = [int(x) for x in parts[1::2]]
    cow_pairs = list(zip(names, milk_amount))
    cow_pairs.sort(key=lambda x: x[1])
    smallest = cow_pairs[0][1]
    second_amount = None

    for name, amt in cow_pairs:
        if amt > smallest:          
            second_amount = amt
            break
if second_amount is not None:
    print("TIE"/n)
else:
    cow_pairs = list(zip(names, milk_amount))
    cow_pairs.sort(key=lambda x: x[1])
print(cow_pairs[0][0], cow_pairs[1][0])d