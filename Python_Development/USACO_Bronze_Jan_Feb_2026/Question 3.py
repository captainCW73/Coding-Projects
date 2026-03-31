n, q = map(int, input().split())
prices = list(map(int, input().split()))

# Preprocess: prices[i] should be min of itself or 2 * prices[i-1]
# Because deal i gives 2x buckets of deal i-1
for i in range(1, n):
    prices[i] = min(prices[i], 2 * prices[i - 1])

results = []
for _ in range(q):
    x = int(input())
    
    total_cost = 0
    remaining = x
    best = float('inf')

    for i in range(n - 1, -1, -1):
        buckets = 2 ** i
        price = prices[i]
        
        if remaining > 0:
            round_up = (remaining + buckets - 1) // buckets
            best = min(best, total_cost + round_up * price)
            
            times = remaining // buckets
            total_cost += times * price
            remaining -= times * buckets
        else:
            best = min(best, total_cost)

    results.append(best)
for result in results:
    print(result)