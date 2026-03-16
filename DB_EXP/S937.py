# S937.py
# 姓名，生日,宿舍使用Faker库生成(但是Faker好像不能生成4个字的名字。。与实际不符)
# 学号使用random生成
# 身高注意要实现正态分布，以及保留小数点后两位（不要舍去末位的0）
# 性别只有男女之分

import random
import numpy as np
from faker import Faker
fake = Faker()

data_size = 5000

snumber_list = []
sname_list = []
sex_list = []
bdate_list = []
height_list = []
dorm_list = []

snumber_exist = ['01032010', '01032023', '01032001', '01032005', '01032112', '03031011', '03031014', '03031051', '03031009', '03031033', '03031056'] 
dorm_exist = ['东 6 舍 221', '东 6 舍 221', '东 1 舍 312', '东 1 舍 312', '东 6 舍 221', '东 2 舍 104', '东 18 舍 421', '东 18 舍 422', '东 2 舍 104', '东 18 舍 423', '东 2 舍 305']

# 女生住东 1-东 5 男生住东 14-18
# 假设每栋楼 8 层 每层 25 间宿舍 每间宿舍至多 4 人
dorm_male = {}
building_male = ['东 6 舍 ', '东 8 舍 ', '东 9 舍 ', '东 18 舍 ', '西 3 舍 ' , '西 4 舍 ' , '西 11 舍 ' , '西 15 舍 '] 
for building in building_male:
    for i in range(1, 9):
        for j in range(1, 26):
            dorm_male[f'{building}{i*100+j}'] = 4

dorm_female = {}
building_female = ['东 1 舍 ', '东 2 舍 ', '东 7 舍 ','西 18 舍 ']
for building in building_female:
    for i in range(1, 9):
        for j in range(1, 26):
            dorm_female[f'{building}{i*100+j}'] = 4 

for dorm in dorm_exist:
    if dorm in dorm_male:
        dorm_male[dorm] -= 1
    elif dorm in dorm_female:
        dorm_female[dorm] -= 1

# 随机生成学生信息
fake = Faker('zh_CN') 
for i in range(data_size):
    
    # 生成学号
    random_snumber = random.randint(1000001, 09999999)
    snumber = f'{random_snumber:08}'       # 格式化学号为字符串，保证长度为 8 位，不足的部分在前面补 0
    while snumber in snumber_exist:
        random_snumber = random.randint(1000001, 09999999)
        snumber = f'{random_snumber:08}'
    snumber_exist.append(snumber)
    
    # 按照男女比例 7：3 生成数据
    if i % 10 <= 6:
        sname = fake.name_male()
        sex = '男'

        # 生成的随机数大多数在 170 到 185 之间
        mean = 177.5  # 平均值
        std_dev = 5  # 标准差

        # 生成符合正态分布的随机数
        random_number = round(random.gauss(mean, std_dev), 2)
        # 将随机数转换为字符串并保留两位小数
        height = "{:.2f}".format(random_number)

       # height = random.choice([random_number])



        # 分配宿舍
        dorm = fake.random.sample(list(dorm_male.keys()), 1)[0]
        while dorm_male[dorm] == 0:
            dorm = fake.random.sample(list(dorm_male.keys()), 1)[0]
        dorm_male[dorm] -= 1
    else:
        sname = fake.name_female()
        sex = '女'

        # 生成的随机数大多数在 155 到 170 之间
        mean = 162.5  # 平均值
        std_dev = 5  # 标准差

        # 生成符合正态分布的随机数
        random_number = round(random.gauss(mean, std_dev), 2)
        # 将随机数转换为字符串并保留两位小数
        height = "{:.2f}".format(random_number)

        
        # 分配宿舍
        dorm = fake.random.sample(list(dorm_female.keys()), 1)[0]
        while dorm_female[dorm] == 0:
            dorm = fake.random.sample(list(dorm_female.keys()), 1)[0]
        dorm_female[dorm] -= 1
    # 随机生日
    bdate = fake.date_of_birth(minimum_age=16, maximum_age=24).strftime('%Y-%m-%d')

    snumber_list.append(snumber)
    sname_list.append(sname)
    sex_list.append(sex)
    bdate_list.append(bdate)
    height_list.append(height)
    dorm_list.append(dorm)
    
# 保存数据 
with open('S937.txt', mode='w', encoding='utf-8') as f: 
    for i in range(data_size):
        f.write(snumber_list[i] + ' ') 
        f.write(sname_list[i] + ' ') 
        f.write(sex_list[i] + ' ') 
        f.write(bdate_list[i] + ' ') 
        f.write(str(height_list[i]) + ' ') 
        f.write(dorm_list[i] + '\n')
