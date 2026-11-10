n = int(input())
a = list(map(int, input().split()))
now = 1
res = 1
for i in range(1, n):    
  if a[i] == a[i-1] + 1:        
    now += 1    
  else:        
    now = 1    
  if now > res:        
      res = now
print(res)
