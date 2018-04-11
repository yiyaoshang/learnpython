#encoding=utf-8
__author = 'heathu'

import sys
import pystache
import os
import time
import config
import subprocess

###############################################################
#                          程序说明                           #
#用于生成从集市ALL取某一天的数据灌入到当天的存储过程          #
###############################################################

#获取数据库返回值
def table_info(table_name):
    table_info = config.con_DB().cursor().execute("SELECT t1.SCM,t1.FILE_TABLE_NAME,t2.COL_NAME\
                                            FROM EU_TAB_PARAM t1 \
                                            INNER JOIN EU_COL_PARAM t2\
                                            ON t1.FILE_TABLE_NAME = t2.FILE_TABLE_NAME\
                                            WHERE t1.FILE_TABLE_NAME = '"+table_name+"'\
                                            ORDER BY t2.COL_SEQ").fetchall()
    return  table_info

#获取列名及字段类型信息
def column_info(table_info):
    col_info = []
    for i,column in enumerate(table_info):
        b = {}
        if i != len(table_info) - 1:
            b["col"] = column[2] + ","
            col_info.append(b)
        else:
            b["col"] = column[2] 
            col_info.append(b)
    return col_info

#建存储过程
def sp_f_sdm(table_info):
    tab_schema = table_info[0][0]
    tname = table_info[0][1]
    sp_name = 'SP_' + tname + '_GET_DATE'
    col_info = column_info(table_info)
    fdm_info = {
        "src" : tab_schema,
        "scm" : tab_schema,
        "tname" : tname,
        "col_info": col_info
    }
    open_fdm_mode = open(config.model_path + "sp_get_date.mustache", 'r')
    filecontent = pystache.render(open_fdm_mode.read(), fdm_info)
    with open(filePath + sp_name + '.sql', 'w') as file_object:
        file_object.write(filecontent)

#创建目录
def mk_path():
    global filePath
    now = time.strftime('%Y%m%d_%H%M',time.localtime(time.time()))
    filePath = config.fgmPath+'/'+now+'/'
    if os.path.isdir(filePath):
        print("filePath is exists")
    else:
        os.makedirs(filePath)
    return filePath

#主程序
def create_tab(tname):
    tab_info = table_info(tname)
    sp_f_sdm(tab_info)

def begin():
    path = mk_path()
    sql = "SELECT file_table_name FROM EU_TAB_PARAM WHERE file_table_name like 'M_%'"
    table_info = config.con_DB().cursor().execute(sql).fetchall()
    for table in table_info:
        tname = table[0]
        print(tname)
        create_tab(tname)
    return path

if __name__=='__main__':
    s = begin()
    print(s)
