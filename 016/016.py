#/usr/bin/python
#encoding=utf-8
'''
author="heathu"
time=20180411
#纯文本文件 number.txt为学生信息, 里面的内容（包括花括号）如下所示
'''
import xlwt
import json

def load_data(file):
    with open(file,encoding='utf-8') as f:
        sdict = json.load(f)
    return sdict

def write_excel(file,xlsname):
    sdict = load_data(file)
    wb = xlwt.Workbook()
    ws = wb.add_sheet('student')
    row = 0
    for list in sdict:
        l = len(list)
        for i in range(l):
            ws.write(row,i,list[i])
        row +=1
    wb.save(xlsname)
    
if __name__=="__main__":
    write_excel('number.txt','number.xls')
