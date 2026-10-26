# n,x=map(str,input().split())
# count=[]
# for i in range(1,int(n)+1):
#     for j in str(i):
#         count.append(j)
# print(count.count(x))
n,x=map(int,input().split())
print(sum(str(i).count(str(x)) for i in range(1,n+1)))

