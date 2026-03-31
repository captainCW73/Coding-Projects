numW = 0
numL = 0
for i in range(6):
    player = input("")
    if player.upper() == "W":
        numW += 1
    elif player.upper() == "L":
        numL += 1
if numW>=5:
    print("1")
elif numW>=3:
    print("2")
elif numW>=1:
    print("3")
else:
    print("-1")
