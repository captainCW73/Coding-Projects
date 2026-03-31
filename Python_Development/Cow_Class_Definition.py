direction = input("").upper()
start = 0
for i in range(len(direction)):
    if direction[i] == "L":
        start -= 1
    elif direction[i] == "R":
        start += 1
print(start)  
