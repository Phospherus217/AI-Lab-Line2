n = int(input())
while n != 1:    
    if n % 2 == 1:        
        new_n = n * 3 + 1        
        print(f"{n}*3+1={new_n}")        
        n = new_n    
    else:        
        new_n = n // 2        
        print(f"{n}/2={new_n}")        
        n = new_n
print("End")
