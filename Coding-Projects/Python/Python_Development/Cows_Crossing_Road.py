lines = int(input())

last_position = {}   # cowid -> last position
crossed_road = 0

for _ in range(lines):
    cowid, position = map(int, input().split())

    if cowid in last_position:
        if last_position[cowid] != position:
            crossed_road += 1

    last_position[cowid] = position

print(crossed_road)
