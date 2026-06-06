firstint = int(input(""))
secondint = int(input(""))
arithchoice = input("Please pick an arithmetic operation (+, -, *, /): ")
if arithchoice == "+":
    print(firstint + secondint)
elif arithchoice == "-":
    print(firstint - secondint)
elif arithchoice == "*":           
    print(firstint * secondint)
elif arithchoice == "/":
    print(firstint / secondint)
else:
    print("Invalid operation")