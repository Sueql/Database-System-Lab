# S937.py
# 姓名，生日,宿舍使用Faker库生成(但是Faker好像不能生成4个字的名字。。与实际不符)
# 学号使用random生成
# 身高注意要实现正态分布，以及保留小数点后两位（不要舍去末位的0）
# 性别只有男女之分

import random
import numpy as np
from faker import Faker
fake = Faker()

# 已有数据
snumber_exist = ['01032010', '01032023', '01032001', '01032005', '01032112', '03031011', '03031014', '03031051', '03031009', '03031033', '03031056'] 
dorm_exist = ['东 6 舍 221', '东 6 舍 221', '东 1 舍 312', '东 1 舍 312', '东 6 舍 221', '东 2 舍 104', '东 18 舍 421', '东 18 舍 422', '东 2 舍 104', '东 18 舍 423', '东 2 舍 305']
# 存放数据的列表
snumber_data = []
sname_data = []
sex_data = []
bdate_data = []
height_data = []
dorm_data = []

n = 5000     #生成数据的条数
dorm_male = {}
building_male = ['东 6 舍 ', '东 8 舍 ', '东 9 舍 ', '东 18 舍 ', '西 3 舍 ' , '西 4 舍 ' , '西 11 舍 ' , '西 15 舍 ']   # 男生宿舍：东 6 舍 , 东 8 舍 , 东 9 舍 , 东 18 舍, 西 3 舍  , 西 4 舍  , 西 11 舍  , 西 15 舍  
for building in building_male:
    for i in range(1, 7):      # 每栋宿舍楼的1-6层为学生宿舍
        for j in range(1, 33):    # 每一层有32间学生宿舍
            dorm_male[f'{building}{i*100+j}'] = 4     # 每个宿舍至多住4名学生

dorm_female = {}
building_female = ['东 1 舍 ', '东 2 舍 ', '东 7 舍 ','西 12 舍 ']    # 女生宿舍：东 1 舍 , 东 2 舍 , 东 7 舍 ,西 12 舍 
for building in building_female:
    for i in range(1, 7):
        for j in range(1, 33):
            dorm_female[f'{building}{i*100+j}'] = 4 

for dorm in dorm_exist:
    if dorm in dorm_male:
        dorm_male[dorm] -= 1
    elif dorm in dorm_female:
        dorm_female[dorm] -= 1

# 生成随机数据
fake = Faker('zh_CN') 
for i in range(n):
    
    # 生成学号
    random_snumber = random.randint(1000001, 9999999)
    # 格式化学号为字符串，保证长度为 8 位，不足的部分在前面补 0
    snumber = f'{random_snumber:08}'
    while snumber in snumber_exist:
        random_snumber = random.randint(1000001, 9999999)  # 生成的学号范围是(01000000，10000000)，不含端点  
        snumber = f'{random_snumber:08}'
    snumber_exist.append(snumber)

    # 生成生日
    bdate = fake.date_of_birth(minimum_age=16, maximum_age=24).strftime('%Y-%m-%d')

    # 随机生成性别，姓名，身高，宿舍（后三个属性取决于性别）
    sex = random.choice(['男', '女'])
    if sex == '男':
        # 根据性别调用fake.name_male()或fake.name_female()分配姓名
        sname = fake.name_female()
        
        # 生成身高
        mean = 177.5  # 平均值，生成的随机数大多数在 170 到 185 之间
        std_dev = 5  # 标准差
        random_number = round(random.gauss(mean, std_dev)/100, 2)      # 生成符合正态分布的随机数
        height = "{:.2f}".format(random_number)        # 将随机数转换为字符串并保留两位小数

        # 分配宿舍
        dorm = fake.random.sample(list(dorm_male.keys()), 1)[0]
        while dorm_male[dorm] == 0:
            dorm = fake.random.sample(list(dorm_male.keys()), 1)[0]
        dorm_male[dorm] -= 1
        
    elif sex == '女':
        # 根据性别调用fake.name_male()或fake.name_female()分配姓名
        sname = fake.name_female()
        
        # 生成身高
        mean = 162.5  # 平均值,生成的随机数大多数在 155 到 170 之间
        std_dev = 5  # 标准差
        random_number = round(random.gauss(mean, std_dev)/100, 2)   # 生成符合正态分布的随机数
        height = "{:.2f}".format(random_number)        # 将随机数转换为字符串并保留两位小数

        # 分配宿舍
        dorm = fake.random.sample(list(dorm_female.keys()), 1)[0]
        while dorm_female[dorm] == 0:
            dorm = fake.random.sample(list(dorm_female.keys()), 1)[0]
        dorm_female[dorm] -= 1
        
    #一个学生的信息
    snumber_data.append(snumber)
    sname_data.append(sname)
    sex_data.append(sex)
    bdate_data.append(bdate)
    height_data.append(height)
    dorm_data.append(dorm)

    
# 将生成的数据写入文件中
with open('S937.txt', mode='w', encoding='utf-8') as f: 
    for i in range(n):
        f.write(snumber_data[i] + ' ') 
        f.write(sname_data[i] + ' ') 
        f.write(sex_data[i] + ' ') 
        f.write(bdate_data[i] + ' ') 
        f.write(str(height_data[i]) + ' ') 
        f.write(dorm_data[i] + '\n')
        




