# SC937.py
# 根据S937.txt和C937.txt生成SC937.txt

import random

n = 180180   # 数据条数
limit = 200  # 每名学生选课上限 200 门
student_limit = {}  # 学生选课上限字典
primary_key = {}  # 主键字典，用于避免重复
sno_data = []  # 学生编号列表
cno_data = []  # 课程编号列表
grade_data = []  # 成绩列表

i = 0  # 计数器

# 从S937.txt中读取学生数据（仅限前1000行）
#with open('S937.txt', mode='r', encoding='utf-8') as f:
#    student = f.readlines()[:1000]

# 从C937.txt中读取课程数据（仅限前100行）
#with open('C937.txt', mode='r', encoding='utf-8') as f:
#    course = f.readlines()[:100]

# 从S937.txt中读取学生数据（从第1001行开始读）
with open('S937.txt', mode='r', encoding='utf-8') as f:
    student = f.readlines()[1000:]

# 从C937.txt中读取课程数据（从第101行开始读）
with open('C937.txt', mode='r', encoding='utf-8') as f:
    course = f.readlines()[100:]


student_num = len(student)  # 学生数据条数
course_num = len(course)  # 课程数据条数

# 循环生成SC937.txt的数据
while i < n:
    sno = student[random.randrange(student_num)].split(' ')[0]
    if sno not in student_limit:  # 如果学生编号不在学生选课上限字典中
        student_limit[sno] = 0  # 将该学生编号加入学生选课上限字典，并初始化选课数量为0
        
    else:  # 如果学生编号已在学生选课上限字典中
        if student_limit[sno] < limit:  # 如果该学生的选课数量未达到上限
            student_limit[sno] += 1  # 该学生的选课数量加1
            
        else:  # 如果该学生的选课数量已达到上限
            continue  # 跳过本次循环，不生成该学生的选课数据
    
    cno = course[random.randrange(course_num)].split(' ')[0]  # 随机选择一个课程编号
    if (sno, cno) in primary_key:  # 如果该学生和课程的组合已存在于主键字典中
        continue
    
    primary_key[(sno, cno)] = True  # 将该学生和课程的组合加入主键字典
    sno_data.append(sno)  # 将学生编号加入学生编号列表
    cno_data.append(cno)  # 将课程编号加入课程编号列表

    while True:  # 防止生成grade=0.5的数据，这种数据插入数据库时会显示成.5
        grade = round(random.uniform(0, 100) / 0.5) * 0.5   # 生成一个随机成绩（四舍五入到0.5的倍数）
        if grade != 0.5:
            break
    
    grade_data.append('{:.1f}'.format(grade))  # 将成绩加入成绩列表，并保留一位小数
    i += 1
    
# 将生成的数据写入SC937.txt
with open('SC937.txt', mode='w', encoding='utf-8') as f:
    for i in range(n):
        f.write(sno_data[i] + ' ')  # 写入学生编号
        f.write(cno_data[i] + ' ')  # 写入课程编号
        f.write(grade_data[i] + '\n')  # 写入成绩并换行
