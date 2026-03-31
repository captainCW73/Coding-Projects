import sys

input = sys.stdin.readline

def solve():
    n = int(input())
    ids = list(map(int, input().split()))
    
    evens = 0
    odds = 0
    
    for x in ids:
        if x % 2 == 0:
            evens += 1
        else:
            odds += 1
            
    while odds > evens:
        odds -= 2
        evens += 1
        
    if evens > odds + 1:
        evens = odds + 1
        
    print(evens + odds)

solve()