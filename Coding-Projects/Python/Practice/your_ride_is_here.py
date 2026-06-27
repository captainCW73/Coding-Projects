from sys import stdin, stdout
input = stdin.readline
print = stdout.write

comet = input().strip()
groupname = input().strip()

comet_product = 1
for letter in comet:
    comet_product *= ord(letter) - ord('A') + 1

group_product = 1
for letter in groupname:
    group_product *= ord(letter) - ord('A') + 1
if comet_product % 47 == group_product % 47:
    print("GO\n")
else:
    print("STAY\n")