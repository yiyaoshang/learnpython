#/usr/bin/python
#encoding=utf-8
'''
author="heathu"
time=20180411
#将 第 0016 题中的 numbers.xls 文件中的内容写到 numbers.xml 文件中，如下
'''
import xlrd
import json
from lxml import etree

def read_excel(file_name):
    exl = xlrd.open_workbook(file_name)
    exl_sheet = exl.sheet_by_name('student')
    data = []
    for i in range(exl_sheet.nrows):
        data.append(exl_sheet.row_values(i))
    return json.dumps(data, ensure_ascii=False, separators=(',', ': '))

def save_xml(data,xml_name):
    root = etree.Element('root')
    citys = etree.SubElement(root,'number')
    citys.text = data
    citys.append(etree.Comment("""一些数字"""))
    citys_xml = etree.ElementTree(root)
    citys_xml.write(xml_name,pretty_print=True,xml_declaration=True,encoding='utf-8')

if __name__=="__main__":
    data = read_excel('./number.xls')
    print(data)
    save_xml(data,'./number.xml')
