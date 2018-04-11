#encoding = utf-8
__author="heathu"
###############################################################
#                          程序说明                           #
#程序参数 参数1 tablename :                                   #
#         如指定ALL表示全量创建，如指定表名则按表明创建       #
#         参数2 date :                                        #
#         表示生成文件夹的日期                                #
#程序示例 python cre_os_tab_v2.py  ALL  20180201              #
#用途：   1.用于生成O层建表语句                               #
#         2.生成S层建表语句                                   #
#         3.生成O层存历史的存储过程                           #
#         4.生成S层转码的存储过程                             #
###############################################################


import sys
import pystache
import os
import subprocess
import config
import time

def conn_db():
    user,passwd,sid = config.dbuser,config.dbpasswd,config.dbsid
    conn = cx_Oracle.connect(user,passwd,sid)
    cursor = conn.cursor()
    return conn,cursor

def get_info(table_name):
    conn = config.con_DB()
    sql = "SELECT T1.elk_table_name,t2.col_seq,t2.col_name,t2.col_type \
           FROM eu_tab_param t1 \
           INNER JOIN eu_col_param t2 ON t1.file_table_name = T2.file_table_name\
           WHERE T1.elk_table_name = '"+table_name+"'  ORDER BY COL_SEQ"
    table_info = conn.cursor().execute(sql).fetchall()
    return table_info
    
def cre_ft_out(table_info):
    tname=table_info[0][0]
    col_info = []
    i = 0
    for column in table_info:
        b = {}
        i=i+1
        if(i==len(table_info)):
            b["col"] = column[2]+"    "+column[3]+"     "
            col_info.append(b)
        else:
            b["col"] = column[2]+"    "+column[3]+"   ,  "
            col_info.append(b)
    fdm_info={
        "scm":config.table_scm,
        "tname":tname,
        "col_info":col_info,
        "etl_ip":config.ft_out_ip
    }
    if tname in ('G_CST_SMY','S_CM_PUB_CODE_REL','CS_M_LM_PM_SHD','CS_M_OVERDUE_LOAN_INFO_DETL','CS_M_LOAN_INFORMATION','CS_M_LM_SETLMT_LOG','CS_F_PTY_INDIV_REL','CS_M_CUSTOMER_INFORMATION'):
        open_fdm_mode=open(config.model_path+"ft_out_2.mustache",'r')
        filecontent=pystache.render(open_fdm_mode.read(),fdm_info)
        with open(filePath+"FT_"+tname+'.sql','w') as file_object:
            file_object.write(filecontent)
    else:
        open_fdm_mode=open(config.model_path+"ft_out.mustache",'r')
        filecontent=pystache.render(open_fdm_mode.read(),fdm_info)
        with open(filePath+"FT_"+tname+'.sql','w') as file_object:
            file_object.write(filecontent)
    print("生成完毕:"+tname)
 
def get_cre_tab1():
    filePath = mk_path()
    conn = config.con_DB()
    table_names = conn.cursor().execute("SELECT elk_table_name FROM eu_tab_param").fetchall()
    for table_name in table_names:
        tname = table_name[0]
        print(tname)
        table_info = get_info(tname)
        cre_ft_out(table_info)
    return filePath   

def merge_sql(filePath):
    print(filePath)
    out_file = '/home/use/elk_prog/table/merge_ft_out_sql/'
    if os.path.isdir(out_file):
        print('filepath is exists')
    else:
        os.makedirs(out_file)
    cat1 = 'cat '+filePath +'*.sql > ' + out_file + 'bi_ft_out.sql'
    subprocess.call(cat1,shell=True)

def mk_path():
    global filePath
    now = time.strftime('%Y%m%d_%H%M',time.localtime(time.time()))
    filePath = config.ftPath+'/'+now+'/'
    if os.path.isdir(filePath):
        print("filePath is exists")
    else:
        os.makedirs(filePath)
    return filePath

def remove():
    if os.path.isdir(config.ftPath):
        print('filepath is exists,truncate')
    else:
        os.makedirs(config.ftPath)
    for file in os.listdir(config.ftPath):
        targetfile = os.path.join(config.ftPath,file)
        if os.path.isfile(targetfile):
            os.remove(targetfile)
#获取输入参数
def get_param():
    #判断输入参数数量是否匹配
    if len(sys.argv) > 3:
        print("输入格式为： 目标表名[ALL] [更新日期] ")
        print("参数不符")
        sys.exit(1)
    #声明使用全局变量
    global tab_info,update_date,filePath,table_names
    conn = config.con_DB()
    tab_info ='ALL' if len(sys.argv) == 1 else sys.argv[1]
    update_date = '' if len(sys.argv) <= 2 else sys.argv[2]
    filePath = config.ftPath+"/ALL/" if len(sys.argv) <= 2 else config.ftPath+"/"+update_date+"/"
    tablenames = conn.cursor().execute("SELECT elk_table_name FROM eu_tab_param").fetchall()
    table_names = []
    for table_name in tablenames:
        table_names.append(table_name[0])
    #判禖件夹是否存在
    if os.path.exists(filePath):
        print("文件夹已经存在")
    else:
        os.makedirs(filePath)
        print("文件夹已创建")
    #判断输入日期是否规范
    if len(update_date)!=0 and not config.isVaildDate(update_date):
        print("日期格式不对")
        sys.exit(2)
    #判断表名是否正确规范
    if tab_info !='ALL' and tab_info not in table_names:
        print("输入表名不存在")
        sys.exit(2)

def get_cre_tab():
    if tab_info == "ALL":  
        for table_name in table_names:
            print(table_name)
            table_info = get_info(table_name)
            cre_ft_out(table_info)
    else:
        table_name = tab_info
        print(table_name)
        table_info = get_info(table_name)
        cre_ft_out(table_info)


if __name__=='__main__':
    get_param()
    get_cre_tab()
    #merge_sql(s)
