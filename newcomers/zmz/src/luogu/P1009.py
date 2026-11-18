n = int(input())
s = 0
jc = 1   # 保存当前i的阶乘
for i in range(1, n+1):    
    jc = jc * i    
    s = s + jc
print(s)
