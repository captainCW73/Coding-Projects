from sys import stdin, stdout
input = stdin.readline
output = stdout.write
zodiacs = ["Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig", "Rat"]
cow = {'Bessie' : 0}
n = int(input())
for _ in range (n):
    parts = input().split()
    cow1 = parts[0]
    direction = parts[3]
    zodiac = parts[4]
    cow2 = parts[7]
    ref_year = cow[cow2]
    ref_index = ref_year % 12
    zodiac_index = zodiacs.index(zodiac)
    if direction == "previous":
        if zodiac_index < ref_index:
            diff = zodiac_index - ref_index
            cow[cow1] = ref_year - diff
        else:
            diff = (ref_index - 12) - zodiac_index
            cow[cow1] = ref_year - diff
    if direction == "next":
        if zodiac_index > ref_index:
            diff = ref_index - zodiac_index
            cow[cow1] = ref_year - diff
        else:
            diff = (ref_index + 12) - zodiac_index
            cow[cow1] = ref_year - diff
print(abs(cow['Elsie']))