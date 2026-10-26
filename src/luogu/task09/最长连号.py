long=int(input())
nums=[int(x) for x in input().split()]
a=[]
b=[]
for i in range(long-1):
    if nums[i]+1==nums[i+1]:
        a.append(nums[i])
    else:
        b.append(len(a))
        a.clear()
        a.append(nums[i])
    b.append(len(a))
print(max(b))









