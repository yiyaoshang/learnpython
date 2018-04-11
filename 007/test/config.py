#encoding:utf-8

import os 
import cx_Oracle
import sqlite3

#配置文件，配置数据库地址，生成建表语句地址

#获取文件所在文件夹
path=os.path.split(os.path.realpath(__file__))[0]
sep=os.sep

#create_os_tab
dbuser='ods_use'
dbpasswd='ods_use'
dbsid='20.4.17.20/edwdb'
ft_in_ip='20.4.17.16'
#model_path='/home/use/elk_prog/table/create_tab/templates/'
#cre_tab_path='/home/use/elk_prog/table/create_tab/etl/os/'

cre_tab_path=path.replace("code_source","sql_files")+sep+"os"+sep
model_path=path.replace("code_source","templates")+sep

#create_ft_tab
table_scm = 'edw_ft_out'
ft_out_ip = '20.4.17.16'
#ftPath='/home/use/elk_prog/table/create_tab/etl/ft_out/'
ftPath=path.replace("code_source","sql_files")+sep+"ft_out"+sep

#create fgm tab
#fgmPath = '/home/use/elk_prog/table/create_tab/etl/fgm/'
fgmPath=path.replace("code_source","sql_files")+sep+"fgm"+sep

#postgre
user="edw_it"
passwd="jcfcedw_123"
dbip="20.4.18.13"

#filePath
ExcelPath = path.replace("code_source","database")+sep+"Excel"+sep
SqlPath = path.replace("code_source","database")+sep+"Sql"+sep
DBPath = path.replace("code_source","database")+sep+"DB"+sep

#print(DBPath)


#连接数据库
def con_DB():
    con_DB =sqlite3.connect(DBPath+'etldb.db')
    #con_DB = cx_Oracle.connect(dbuser,dbpasswd,dbsid)
    return con_DB

#验证日期格式是否正确
def isVaildDate(date):
    try:
        if ":" in date:
            time.strptime(date, "%Y-%m-%d %H:%M:%S")
        elif "-" in date:
            time.strptime(date, "%Y-%m-%d")
        else:
            time.strptime(date, "%Y%m%d")
        return True
    except:
        return False

#获取N个空格
def getNSpace(col_name, fix_len):
    re_str = ""
    if (fix_len - len(col_name) < 1):
        print("col_name lenger fix_len")
        exit(1)
    for index in range(1, fix_len - len(col_name)):
        re_str = re_str + " "
    return re_str