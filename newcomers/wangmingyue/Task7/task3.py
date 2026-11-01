def is_pass(score, pass_score=60):
    if score>=pass_score:
        return True
    else:
        return False
print(is_pass(59))      
print(is_pass(60))      
print(is_pass(75, 80))    

def add_scores(*scores):
    total = 0
    for score in scores:
       total += score
    return total
print(add_scores(80, 90))      
print(add_scores(60, 70, 80))  
print(add_scores())           

def show_students(**info):
    print(info.get('name','未填写'))
    print(info.get('age','未填写'))
    print(info.get('city','未填写'))
show_students(name='小王',age=18,city='晋中')
show_students(age=18,name='小李')