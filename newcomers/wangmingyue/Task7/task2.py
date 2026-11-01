python_students = ["小王", "小李", "小王", "小张"]#列表
java_students = ["小李", "小刘", "小陈", "小刘"]
def analyze_courses(python_students, java_students):
    students1=set(python_students)
    students2=set(java_students)
    both=students1 & students2 
    everyone=students1 | students2
    python_only=students1 - students2
    java_only=students2 - students1
    return {
        "students1": students1,
        "students2": students2,
        "both": both,
        "everyone": everyone,
        "python_only": python_only,
        "java_only": java_only
    }
result = analyze_courses(python_students, java_students)
print(f'转换为集合去重{result["students1"]},{result["students2"]}')    
print(f'同时学习python和java的学生有:{result["both"]}')
print(f'所有学生有:{result["everyone"]}')
print(f'只学习python的学生有:{result["python_only"]}')
print(f'只学习java的学生有:{result["java_only"]}')