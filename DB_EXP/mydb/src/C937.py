# C937.py
# 先进行爬虫
# 然后处理一下数据格式，得到可以插入MYDB的数据

import time
import random
import re
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service  # 导入Service类

# 开始爬虫 #############################################################################################################

options = Options()  ## 设置Firefox选项

# 指定geckodriver路径并创建WebDriver
service = Service(r'C:\Program Files\Mozilla Firefox\geckodriver.exe')
driver = webdriver.Firefox(service=service, options=options)

NetID = None     # 学号
password = None

# 打开本科教务平台
url = 'http://ehall.xjtu.edu.cn/new/index.html?browser=no'
driver.get(url)

# 登录
login_button = driver.find_element(By.ID, 'ampHasNoLogin')  # 定位登录按钮
login_button.click()  # 点击登录按钮

# 输入NetID和密码
user_box = driver.find_element(By.NAME, 'username')  # 定位学号输入框
password_box = driver.find_element(By.NAME, 'pwd')  # 定位密码输入框
user_box.send_keys('2202321937')    # 这里输入我的学号
password_box.send_keys('xxxish0125.')      # 这里输入我的密码

# 进入统一身份认证网关
login_button = driver.find_element(By.CSS_SELECTOR, '.loginState > #account_login')  # 定位统一身份认证网关登录按钮
driver.execute_script('arguments[0].click();', login_button)  # 执行点击“登录”按钮操作

# 查询全校课表
time.sleep(3) 
app_list = driver.find_element(By.CSS_SELECTOR, '.amp-aside-box-mini-item > .icon-liebiao1')  # 定位全校课表查询按钮
driver.execute_script('arguments[0].click();', app_list)  # 执行点击操作

course_table = driver.find_element(By.CSS_SELECTOR, '.appFlag:nth-child(10) > .amp-str-cut')  # 定位课程表按钮
driver.execute_script('arguments[0].click();', course_table)  # 执行点击操作

# 显示新的浏览器窗口
new_window = driver.window_handles[-1]  # 获取新打开的窗口句柄
driver.switch_to.window(new_window)  # 切换到新窗口

# 爬取数据
with open('C937_crawler.txt', mode='w') as f:  # 打开文件进行写入
    for i in range(400):  # 循环400次：可以获得4000条课程信息（因为一个课程号可能对应很多条重复的课程信息，它们之间只有课序号不同）循环300次时只能得到789条有效数据。。。
        time.sleep(8)
        for j in range(10):  # 循环10次：因为每页10条课程信息
            cnumber = f'id("row{j}qxkcb-index-table")/TD[2]/SPAN[1]'  # 获取课程编号
            cname = f'id("row{j}qxkcb-index-table")/TD[3]/SPAN[1]'  # 获取课程名称
            period = f'id("row{j}qxkcb-index-table")/TD[4]/SPAN[1]'  # 获取学时
            credit = f'id("row{j}qxkcb-index-table")/TD[5]/SPAN[1]'  # 获取学分
            teacher = f'id("row{j}qxkcb-index-table")/TD[6]/SPAN[1]'  # 获取教师姓名
            f.write(driver.find_element(By.XPATH, cnumber).get_attribute('title') + '; ')  # 写入课程编号
            f.write(driver.find_element(By.XPATH, cname).get_attribute('title') + '; ')  # 写入课程名称
            f.write(driver.find_element(By.XPATH, period).get_attribute('title') + '; ')  # 写入学时
            f.write(driver.find_element(By.XPATH, credit).get_attribute('title') + '; ')  # 写入学分
            f.write(driver.find_element(By.XPATH, teacher).get_attribute('title') + '\n')  # 写入教师姓名并换行
            next_page = driver.find_element(By.CSS_SELECTOR, '#pagerqxkcb-index-table .icon-keyboardarrowright')  # 定位下一页按钮
            driver.execute_script('arguments[0].click();', next_page)  # 点击下一页按钮

driver.quit()  # 退出浏览器


# 开始转换数据格式，将生成的数据写入C937.txt ###################################################################################

n = 1043     # 数据条数(因为只保留了老师名字为汉字的数据) 经试验发现可以生成1002条数据
# 已有数据
cnumber_exist = ['CS-01', 'CS-02', 'CS-04', 'CS-05', 'EE-01', 'EE-02', 'EE-03']
# 存放数据的列表
cnumber_data = []
cname_data = []
period_data = []
credit_data = []
teacher_data = []
i = 0  # 计数器

# 从文件中按顺序读取数据
with open('C937_crawler.txt', mode='r') as f:
    lines = f.readlines()  # 读取文件的所有行

for line in lines:
    if i >= 1043:
        break  # 如果已经读取了n条数据，则退出循环
    record = line[:-1].split(' ')  # 以空格分割数据
    cname = record[1]  # 获取课程名称
    #teacher = record[5].split(',')[0]  # 获取教师姓名
    teacher = record[4].split(',')[0]  # 获取教师姓名，因为一门课都很多上课时间，有很多重复的老师名字，这里为了简化，只取第一位老师的名字
    # 如果老师姓名为空，则跳过将数据写入C937.txt的步骤
    if teacher == '':
        continue

    if len(cname) > 25 or len(teacher) > 20:  # 检查课程名称和教师姓名长度
        continue  # 如果长度不符合要求则跳过本次循环
    cnumber = record[0]  # 获取课程编号

    # 根据课程编号的前缀进行处理（根据已有的CS和EE）
    if cnumber[:4] == 'COMP':
        cnumber = 'CS'  # 如果是以'COMP'开头，则替换为'CS'
    elif cnumber[:4] == 'EELC':
        cnumber = 'EE'  # 如果是以'EELC'开头，则替换为'EE'
    else:
        cnumber = cnumber[:2]  # 否则保留课程号前两位
    num = abs(hash(record[0][4:10])) % 100  # 计算哈希值并取绝对值再取余数
    cnumber += f'-{num}' if num > 9 else f'-0{num}'  # 根据哈希值拼接课程编号

    # 检查课程编号是否已存在
    if cnumber in cnumber_exist or cnumber in cnumber_data:
        continue
    
    # 检查课程名称是否包含空格(其实并不能有效避免课程名中含空格的情况)
    #if ' ' in cname:
    #   continue

    # 检查课程名称是否含英文，如果含英文就舍弃这条数据
    for w in cname:
        if not '\u4e00' <= w <= '\u9fff':
            continue

    # 获取数据
    period = record[2]  # 获取学时
    credit = record[3]  # 获取学分
    cnumber_data.append(cnumber)  # 将课程编号添加到列表
    cname_data.append(cname)  # 将课程名称添加到列表
    period_data.append(period)  # 将学时添加到列表
    credit_data.append(credit)  # 将学分添加到列表
    teacher_data.append(teacher)  # 将教师姓名添加到列表

    i += 1  # 计数器加一
    

# 判断字符串是否为汉字
def is_chinese(text):
    for char in text:
        if not '\u4e00' <= char <= '\u9fff':
            return False
    return True


# 将处理后的数据写入新文件，仅包含教师姓名为汉字的数据
with open('C937.txt', mode='w', encoding='utf-8') as f:
    for i in range(n):
        if i < len(cnumber_data):  # 检查索引是否在列表范围内
            if is_chinese(teacher_data[i]):  # 检查教师姓名是否为汉字
                f.write(cnumber_data[i] + ' ')  # 写入课程编号
                f.write(cname_data[i].rstrip(';') + ' ')  # 写入课程名称（注意不要把分号写入新文件）
                f.write(period_data[i].rstrip(';') + ' ')  # 写入学时（注意同上）
                f.write(credit_data[i].rstrip(';') + ' ')  # 写入学分（注意同上）
                f.write(teacher_data[i] + '\n')  # 写入教师姓名并换行
