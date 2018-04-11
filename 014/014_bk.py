#/usr/bin/python
#encoding=utf-8
'''
author="heathu"
time=20180411
#纯文本文件 student.txt为学生信息, 里面的内容（包括花括号）如下所示
'''
import xlwt
import json
from collections import  OrderedDict

with open('student.txt',encoding='utf-8') as f:
    students_dict = OrderedDict(json.load(f))
    print(students_dict)

wb = xlwt.Workbook()  #创建一个工作簿
ws = wb.add_sheet('student') #创建一个sheet

row = 0
for k,v in students_dict.items():
    ws.write(row,0,k)
    col = 1
    for item in v:
        ws.write(row,col,item)
        col += 1
    row +=1
wb.save('student.xls')

    
