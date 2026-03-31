n, q = map(int, input().split())
prices = list(map(int, input().split()))
results = []
for _ in range(q):
    x = int(input())
    
    total_cost = 0
    remaining = x
    

    for i in range(n - 1, -1, -1):
        buckets = 2 ** i
        price = prices[i]
        
        if remaining > 0:
            times = remaining // buckets
            total_cost += times * price
            remaining -= times * buckets
            
    results.append(total_cost)
for result in results:
    print(result)