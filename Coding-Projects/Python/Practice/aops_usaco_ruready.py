from sys import stdin, stdout

nk = input().split()
n = int(nk[0])
k = int(nk[1])
num_list = []
start = 1

def has_duplicates(my_list):
    return len(my_list) != len(set(myx_list))

for i in range(n):
    value = start * start
    num_list.append(value)
    start += 1

for i in range(k):
    if has_duplicates(num_list):    
        num_list[-1] = num_list[-1] // 2 
        num_list[-1].replace(num_list[-1], num_list[-1] // 2)
