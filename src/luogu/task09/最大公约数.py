a,b,c=map(int,input().split())
def calculate(num):
    factor=set()
    for i in range(1,num+1):
        if num%i==0:
            factor.add(i)
            factor.add(num//i)
    return factor

print(max(list(calculate(a)&calculate(b)&calculate(c))))
