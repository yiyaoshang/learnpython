# -*- encoding=utf-8 -*-
__author = "heathu"
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

import pystache
import config
import sys
import os
import time
import subprocess

#表模式及表空间
tab_in_o = "cmis"
tab_in_s = "edw_it_s"
tab_ft_in = "edw_ft_in"
tab_ft_out = "edw_ft_out"
tablespace = "edw_tbs"


#获取表字段
def get_tab_info(table_name):
    table_info = config.con_DB().cursor().execute("SELECT t1.table_name,t1.sys_id,t1.table_cn_name,t1.src_table_name,"
                                   "t2.column_name,t2.ods_column_type,t2.change_rule,"
                                   "t2.column_cn_name,t1.hash_col,t1.part_col,t2.is_code,t1.etl_stg,t2.is_pri,t1.incr_crt"
                                   " FROM table_param t1 ,column_param t2 "
                                   "where t1.table_name =t2.table_name and t1.table_name ='" + table_name + "' order by t2.col_seq").fetchall()
    return table_info

#获取表注释
def comment_info(table_info):
    com_info=[]
    a = {}
    if(table_info[0][2] != None):
        a['com'] =" COMMENT '{}'".format(table_info[0][2])
        com_info.append(a)
    return com_info

#获取列信息
def column_info(table_info):
    col_info=[]
    for i,column in enumerate(table_info):
        b={}
        if i != len(table_info) - 1:
            b["col"] = column[4]+"    "+column[5]+"   COMMENT '"+column[7]+"'  ,"
            col_info.append(b)
        else:
            b["col"] = column[4]+"    "+column[5]+"   COMMENT '"+column[7]+"'     "
            col_info.append(b)
    return col_info

#创建O层表
def cre_odm(table_info,col_info,com_info):
    etl_stg = table_info[0][11]
    sdmname=table_info[0][0]
    tname=sdmname
    hash_col=table_info[0][8]
    fdm_info={
        "scm":tab_in_o,
        "tname":tname,
        "col_info":col_info,
        "com_info":com_info,
        "hash_col":hash_col,
        "tablespace":tablespace
    }
    open_fdm_mode=open(config.model_path+"odm_01.mustache",'r')
    filecontent=pystache.render(open_fdm_mode.read(),fdm_info)
    with open(filePath+tname+'.sql','w') as file_object:
        file_object.write(filecontent)

#建表主程序
def begin(table_name):
    table_info=get_tab_info(table_name)
    col_info=column_info(table_info)
    com_info=comment_info(table_info)
    cre_odm(table_info,col_info,com_info)

#获取输入参数
def get_param():
    #判断输入参数数量是否匹配
    if len(sys.argv) > 3:
        print("输入格式为： 目标表名[ALL] [更新日期] ")
        print("参数不符")
        sys.exit(1)
    #声明使用全局变量
    global tab_info,update_date,filePath,table_names
    tab_info ='ALL' if len(sys.argv) == 1 else sys.argv[1]
    update_date = '' if len(sys.argv) <= 2 else sys.argv[2]
    filePath = config.cre_tab_path+"/ALL/" if len(sys.argv) <= 2 else config.cre_tab_path+"/"+update_date+"/"
    tablenames = config.con_DB().cursor().execute("SELECT table_name FROM table_param").fetchall()
    table_names = []
    for table_name in tablenames:
        table_names.append(table_name[0])
    #判�文件夹是否存在
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
            begin(table_name)
    else:
        table_name = tab_info
        print(table_name)
        begin(table_name)

if __name__=="__main__":
    get_param()
    get_cre_tab()
    #merge_sql(s)

