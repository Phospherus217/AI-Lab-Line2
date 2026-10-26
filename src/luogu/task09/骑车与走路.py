road=float(input())
def bike(road_):
    return road_/3+50
def walk(road_):
    return road_/1.2
if bike(road)==walk(road):
    print("All")
elif bike(road)<=walk(road):
    print("Bike")
elif bike(road)>=walk(road):
    print("Walk")

