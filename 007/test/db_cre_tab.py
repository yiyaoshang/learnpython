#encoding=utf-8
__author = 'heathu'
###############################################################
#                          程序说明                           #
#程序参数 参数1 path :                                        #
#            sql语句所在目录                                  #
#         参数2 tablename.sql                                 #
#            若无第二个参数，则生成全部文件                   #
#            若有则生成指定文件                               #
#程序示例 python db_cre_tab.py  /home/  CUST_INFO.sql         #
#用途：   1.用于ELK建表                                       #
#         2.用于ELK建存储过程                                 #
###############################################################

import sys
import subprocess
from multiprocessing import Pool
import config

user=config.user
passwd=config.passwd
dbip=config.dbip

def createTable(tableName):
    sql="gsql -U "+user+" -W "+passwd+" -d jcfcedw -p 25108 -h "+dbip+" -f "+tableName
    b =  subprocess.check_output(sql,shell=True)
    print(len(b))
    if len(b) > 32:
        subprocess.call("echo "+tableName+">> success.txt",shell=True)
    else:
        subprocess.call("echo "+tableName+">> failed.txt",shell=True)

def write_sql():
    subprocess.check_call("ls "+path+"/*.sql > a.txt", shell=True)

def main():
    with open('a.txt') as a:
        tableNames = a.readlines()
    pool = Pool(processes=5)
    for tableName in tableNames:
        tableName = tableName.rstrip() 
        pool.apply_async(createTable,(tableName,))
    pool.close()
    pool.join()

#获取输入参数
def get_param():
    #判断输入参数数量是否匹配
    if len(sys.argv) > 3:
        print("输入格式为： 路径 [表名] ")
        print("参数不符")
        sys.exit(1)
    #声明使用全局变量
    global path,table_name
    path = sys.argv[1]
    table_name = '' if len(sys.argv) <= 2 else path+"/"+sys.argv[2]


if __name__ == "__main__":
    get_param()
    write_sql()
    if table_name == '':
        main()
    else:
        createTable(table_name)
