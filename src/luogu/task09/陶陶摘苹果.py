hight=[int(x) for x in input().split()]
hand=int(input())+30
print(len([x for x in hight if hand >= x]))