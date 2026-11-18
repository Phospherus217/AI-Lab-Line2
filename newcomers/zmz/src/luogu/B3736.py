def gcd(a, b):    
    while b != 0:        
        r = a % b        
        a = b        
        b = r    
    return a
x, y, z = map(int, input().split())
res = gcd(gcd(x, y), z)
print(res)
