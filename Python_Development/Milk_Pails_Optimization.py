milk_pours = input()
X, Y, M = [int(x) for x in milk_pours.split()]

max_milk = 0

for i in range(M // X + 1):
    for j in range(M // Y + 1):
        current_total = (i * X) + (j * Y)
        
        if current_total <= M:
            if current_total > max_milk:
                max_milk = current_total

print(max_milk)