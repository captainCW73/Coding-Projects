import sys
input_data = sys.stdin.read().split()
print_out = sys.stdout.write

def solve():
    if not input_data:
        return
    
    it = iter(input_data)
    t_str = next(it, None)
    if t_str is None: return
    t = int(t_str)
    
    ans = []
    
    for _ in range(t):
        n = int(next(it))
        k = abs(int(next(it)))
        a = [int(next(it)) for _ in range(n)]
        
        groups = {}
        for x in a:
            rem = x % k
            if rem not in groups:
                groups[rem] = []
            groups[rem].append(x // k)
            
        total_ops = 0
        for rem in groups:
            vals = sorted(groups[rem])
            m = len(vals)
            
            ElsieNumber = []
            for i in range(m):
                ElsieNumber.append(vals[i] - i)
            
            ElsieNumber.sort()
            median = ElsieNumber[m // 2]
            
            for val in ElsieNumber:
                total_ops += abs(val - median)
        
        ans.append(str(total_ops))

    print_out("\n".join(ans) + "\n")

solve()