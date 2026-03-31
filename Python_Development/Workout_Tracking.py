kn = input("").split()
kandn = [int(x) for x in kn]
number_cows = kandn[1]
numbers = []
for _ in range(kandn[0]):
    numbers_line = input("").split()
    numbers.extend([int(x) for x in numbers_line])
prev_num = None
numoffitcows = 0
for num in numbers:
    if prev_num is not None:
        if prev_num < num:
            numoffitcows += 1
    prev_num = num
print(numoffitcows)    

