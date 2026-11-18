n,x=input().split(" ")
n=int(n)
l=[]
for i in range(1,n+1):    
    l.extend(list(str(i)))
print(l.count(x))
