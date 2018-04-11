#/usr/bin/python
#encoding=utf-8
'''
author="heathu"
time=20180411
#第 0017 题：** 将 第 0014 题中的 student.xls 文件中的内容写到 student.xml 文件中，如
'''
import xlrd
import json
from lxml import etree

def read_excel(file_name):
    exl = xlrd.open_workbook(file_name)
    exl_sheet = exl.sheet_by_name('student')
    data = {}
    for i in range(exl_sheet.nrows):
        data[exl_sheet.row_values(i)[0]] = exl_sheet.row_values(i)[1:]
    return json.dumps(data)

def save_xml(data,xml_name):
    root = etree.Element('root')
    students = etree.SubElement(root,'student')
    students.append(etree.Comment("""学生信息表 "id" : [名字，数学，语文，英语]"""))
    students.text = data
    student_xml = etree.ElementTree(root)
    student_xml.write(xml_name,pretty_print=True,xml_declaration=True,encoding='utf-8')

if __name__=="__main__":
    data = read_excel('./student.xls')
    print(data)
    save_xml(data,'./student.xml')
