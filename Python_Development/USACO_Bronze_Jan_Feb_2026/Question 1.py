def flip(c):
    if c == 'M':
        return 'O'
    else:
        return 'M'

tk = input("").split()
t = int(tk[0])
ElsieTypingMode = int(tk[1])

outputs = []

for i in range(t):
    numletters = int(input(""))
    s = input("")
    
    result = []
    is_flipped = False
    
    for j in range(numletters - 1, -1, -1):
        char = s[j]
        if is_flipped:
            char = flip(char)
        result.append(char)
        if char == "O":
            is_flipped = not is_flipped
    
    outputs.append("YES")
    if ElsieTypingMode == 1:
        outputs.append("".join(result[::-1]))

for output in outputs:
    print(output)