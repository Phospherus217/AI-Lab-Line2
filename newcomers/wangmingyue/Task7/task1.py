students = [
    {"name": "小王", "score": 85},
    {"name": "小李", "score": 58},
    {"name": "小张", "score": 92},
    {"name": "小刘", "score": 76},
]
students[1]['score']=65
students.append({'name':'小陈','score':88})
print(students[:3])
new_students=[student['name'] for student in students if student['score']>=80]
print(new_students)
dict_students={student['name']:student['score'] for student in students}
print(dict_students)
tuple_students=(students[0]['name'],students[0]['score'])
print(tuple_students)
a,b = tuple_students
print(f'姓名：{a},成绩：{b}')