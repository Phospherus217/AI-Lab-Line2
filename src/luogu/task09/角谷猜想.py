enter=int(input())
def calculate(num):
    if num!=1:
        if num%2!=0:
            print(f"{num}*3+1={int(num*3+1)}")
            num=int(num*3+1)
            calculate(num)

        elif num%2==0:
            print(f"{num}/2={int(num/2)}")
            num=int(num/2)
            calculate(num)
    else:
        print("End")
calculate(enter)
