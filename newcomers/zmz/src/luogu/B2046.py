s = int(input())
t_walk = s / 1.2
t_bike = 50 + s / 3.0
if t_bike < t_walk:    
    print("Bike")
elif t_bike > t_walk:    
    print("Walk")
else:    
    print("All")
