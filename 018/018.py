#/usr/bin/python
#encoding=utf-8
'''
author="heathu"
time=20180411
#将 第 0015 题中的 city.xls 文件中的内容写到 city.xml 文件中，如下所示
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
    return json.dumps(data, indent=4, ensure_ascii=False, separators=(',', ': '))

def save_xml(data,xml_name):
    root = etree.Element('root')
    citys = etree.SubElement(root,'citys')
    citys.text = data
    citys.append(etree.Comment("""城市信息"""))
    citys_xml = etree.ElementTree(root)
    citys_xml.write(xml_name,pretty_print=True,xml_declaration=True,encoding='utf-8')

if __name__=="__main__":
    data = read_excel('./citys.xls')
    print(data)
    save_xml(data,'./citys.xml')
