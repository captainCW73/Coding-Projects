nk = input("").split()
n = int(nk[0])
k = int(nk[1])
moves = []
for i in range(k):
    xyz = input("").split()
    x = int(xyz[0])
    y = int(xyz[1])
    z = int(xyz[2])
    moves.append((x, y, z))
max_score = 0
count = 0
for i in range(2**n):
    board = []
    for j in range(n):
        if (i >> j) & 1:
            board.append('O')
        else:
            board.append('M')
    score = 0
    for move in moves:
        x, y, z = move
        if board[x - 1] == 'M' and board[y - 1] == 'O' and board[z - 1] == 'O':
            score += 1
    if score > max_score:
        max_score = score
        count = 1
    elif score == max_score:
        count += 1
print(max_score, count)

            

