#/usr/bin/python
#encoding=utf-8
'''
author="heathu"
time=20180412
#第 0020 题： 登陆中国联通网上营业厅 后选择「自助服务」 --> 「详单查询」，然后选择你要查询的时间段，
点击「查询」按钮，查询结果页面的最下方，点击「导出」，就会生成类似于 2014年10月01日～2014年10月31日
通话详单.xls 文件。写代码，对每月通话时间做个统计。
'''
import xlrd

def count_time(filename):
    wb = xlrd.open_workbook(filename)
    ws = wb.sheet_by_index(0)
    rownums = ws.nrows
    colnums = ws.ncols
    total = 0
    for i in range(1,rownums):
        total += int(ws.cell_value(i,2))
    return total

if __name__=="__main__":
    filename = './src.xlsx'
    total = count_time(filename)
    print(total)
