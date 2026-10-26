n=int(input())
def factorial(n):
    if n==1:
        return 1
    return n*factorial(n-1)
s=0
for i in range(1,n+1):
    s+=factorial(i)
print(s)
