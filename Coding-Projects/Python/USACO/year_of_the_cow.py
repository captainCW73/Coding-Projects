from sys import stdin, stdout
input = stdin.readline
output = stdout.write
zodiacs = ["Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig", "Rat"]
cows = {"Bessie": 0}
num = int(input(""))
for i in range(num):
    states = input("").split()
    cow = states[0]
    bora = states[4]
    zodiac = states[5]
    ref_year = cows[bora]
    ref_zodiac = zodiacs[ref_year % 12]