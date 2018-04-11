#encoding=utf-8
__author = 'heathu'
###############################################################
#                          程序说明                           #
#程序参数 参数1 tablename :                                   #
#         如指定ALL表示全量创建，如指定表名则按表明创建       #
#         参数2 date :                                        #
#         表示生成文件夹的日期                                #
#程序示例 python cre_fgm_tab.py  ALL  20180201                #
#用途：   1.用于生成F层建表语句及存储过程                     #
#         2.用于生成G层建表语句及存储过程                     #
#         3.用于生成M层建表语句及存储过程                     #
#         4.注意这四张表为手工生成                            #
#         'F_PRD_P_FEE_INFO','F_ORG_INSORGINFO',              #
#         'M_WFI_JOIN_INFO','G_LOAN_SMY'                      #
###############################################################

import sys
import pystache
import os
import time
import config
import subprocess

#设置全局变量
global tablespace,conn_db
tablespace = 'edw_tbs'
conn_db = config.con_DB()

#获取数据库返回值
def table_info(table_name):
    table_info = conn_db.cursor().execute("SELECT TAB_NAME,CN_NAME,COL_NAME,COL_COM,COL_TYP,IS_PRI,\
	                                        IS_HASH,GROP,SRC_TAB_NAME,SRC_CN_NAME,SRC_COL_NAME,\
	                                        SRC_COL_COL,SRC_COL_TYP,MAP_RULE,MAP_COM,SRC_SCHEMA,JOIN_TAB,TAB_JC,\
	                                        JOIN_TYP,JOIN_COND,WHERE_COND,TAB_SCHEMA\
                                            FROM H_MAPPING WHERE TAB_NAME ='"+ table_name + "'   ORDER BY ID").fetchall()
    return  table_info

#获取建表信息
def comment_info(table_info):
    tab_schema = table_info[0][-1].lower()
    com_info = []
    tname = table_info[0][0]
    for column in table_info:
        a = {}
        a['com'] = "COMMENT ON COLUMN {}.{}.{} is '{}' ;".format(tab_schema,tname,column[2],column[3])
        com_info.append(a)
    if table_info[0][1] != None:
        a['com'] = "COMMENT ON TABLE {}.{} is '{}';".format(tab_schema,tname, table_info[0][1])
        com_info.extend(a)
    return com_info

#获取列名及字段类型信息
def column_info(table_info):
    col_info = []
    hash_info = []
    for i,column in enumerate(table_info):
        b = {}
        if i != len(table_info) - 1:
            b["col"] = column[2] + "    " + column[4] + ","
            col_info.append(b)
        else:
            b["col"] = column[2] + "    " + column[4]
            col_info.append(b)
        if column[6] == 'Y' or column[6] == 'YES' :
            hash_info.append(column[2])
    return col_info,hash_info

#建表语句
def cre_f_tab(table_info,col_info,hash_col,com_info):
    if len(hash_col)==1:
        hash_col = hash_col[0]
    else:
        hash_col = hash_col[0] + "," + hash_col[1]
    tab_schema = table_info[0][-1].lower()
    tname =  table_info[0][0]
    fdm_info={
        "scm" : tab_schema,
        "t_name" : tname,
        "col_info" : col_info,
        "hash_col": hash_col,
        "tablespace": tablespace,
        "com_info" : com_info
    }
    if tab_schema in ['edw_it_f','edw_it_g']:
        open_fdm_mode = open(config.model_path + "fdm.mustache", 'r')
        filecontent = pystache.render(open_fdm_mode.read(), fdm_info)
        with open(filePath + tname + '.sql', 'w') as file_object:
            file_object.write(filecontent)
    elif tab_schema == 'edw_it_m':
        open_fdm_mode = open(config.model_path + "mdm.mustache", 'r')
        filecontent = pystache.render(open_fdm_mode.read(), fdm_info)
        with open(filePath + tname + '.sql', 'w',encoding="utf-8") as file_object:
            file_object.write(filecontent)


#建存储过程
def sp_f_sdm(table_info):
    tab_schema = table_info[0][21].lower()
    tname = table_info[0][0]
    sp_name = 'SP_' + tname
    col_info = []
    col_join = []
    condition = []
    scol_info = []
    for column in table_info:
        a = {}
        b = {}
        c = {}
        d = {}
        if column[8] != " ":
            src_schema = column[15]
        d["col"] = column[2] + ","
        col_info.append(d)
        s = ''
        if column[13]=="NULL":
            s = "' '"
        else:
            s = column[13]
        if not column[14] or len(column[13]) > 30:
            a["scol"] = s + ","
        else:
            a["scol"] = s + "," + config.getNSpace(column[13], 49) + "--" + column[14]
        scol_info.append(a)
        if column[15] != " " and column[18] is " ":
            b['coljoin'] = column[15]+'.' + column[16] + '  AS ' +  column[17]
            col_join.append(b)
        elif column[15] != " " and column[18] != " " and column[19] != " ":
            b['coljoin'] = column[18]+'  '+column[15]+'.' + column[16] + ' AS ' + column[17] +'  ON '+ column[19]
            col_join.append(b)
        elif column[15] == " " and column[16] != " ":
            b['coljoin'] = column[18]+'  '+column[16] + ' AS ' + column[17] + ' ON ' + column[19]
            col_join.append(b)
        if column[20] is " ":
            pass
        else:
            c['cond'] = column[20]
            condition.append(c)
    fdm_info = {
        "src" : src_schema,
        "scm" : tab_schema,
        "tname" : tname,
        "col_info": col_info,
        "scol_info" : scol_info,
      #  "com_info" : com_info,
        "col_join" : col_join,
        "condition" : condition
    }
    if tab_schema == 'edw_it_g':
        open_fdm_mode = open(config.model_path + "sp_gdm.mustache", 'r')
        filecontent = pystache.render(open_fdm_mode.read(), fdm_info)
        with open(filePath + sp_name + '.sql', 'w') as file_object:
            file_object.write(filecontent)
    elif tab_schema == 'edw_it_m':
        open_fdm_mode = open(config.model_path + "sp_mdm.mustache", 'r')
        filecontent = pystache.render(open_fdm_mode.read(), fdm_info)
        with open(filePath + sp_name + '.sql', 'w') as file_object:
            file_object.write(filecontent)
    elif tab_schema == 'edw_it_f':
        open_fdm_mode = open(config.model_path + "sp_fdm.mustache", 'r')
        filecontent = pystache.render(open_fdm_mode.read(), fdm_info)
        with open(filePath + sp_name + '.sql', 'w') as file_object:
            file_object.write(filecontent)

def create_tab(tab_schema,tname):
    tab_info = table_info(tname)
    col_info,hash_col = column_info(tab_info)
    com_info = comment_info(tab_info)
    cre_f_tab(tab_info,col_info,hash_col,com_info)
    sp_f_sdm(tab_info)

#获取配置信息
def get_param():
    #检查参数个数
    if len(sys.argv) > 3:
        print("example python cre_os_tab [ALL] [DATE]")
        print("please input right param")
        sys.exit(1)
    #设置全局变量
    global tab_info,update_date,filePath,table_names,tab_schema
    tab_info ='ALL' if len(sys.argv) == 1 else sys.argv[1]
    update_date = '' if len(sys.argv) <= 2 else sys.argv[2]
    filePath = config.fgmPath+"/ALL/" if len(sys.argv) <= 2 else config.fgmPath+"/"+update_date+"/"
    tablenames = conn_db.cursor().execute("SELECT distinct tab_name FROM H_MAPPING WHERE tab_name not in ('F_PRD_P_FEE_INFO','F_ORG_INSORGINFO','M_WFI_JOIN_INFO','G_LOAN_SMY')").fetchall()
    table_names = []
    for table_name in tablenames:
        table_names.append(table_name[0])
    #判断文件夹是否存在
    if os.path.exists(filePath):
        print("filePath is exists")
    else:
        os.makedirs(filePath)
        print("filePath is mkdir")
    #检查日期是否有效
    if len(update_date)!=0 and not config.isVaildDate(update_date):
        print("鏃ユ湡鏍煎紡涓嶅")
        sys.exit(2)
    #检查表名是否有效
    if tab_info !='ALL' and tab_info not in table_names:
        print("tablename is vaild")
        sys.exit(2)

def get_cre_tab():
    if tab_info == "ALL":  
        for table_name in table_names:
            tab_schema = 'EDW_IT_'+table_name[:1]
            #print(tab_schema,table_name)
            create_tab(tab_schema,table_name)
            print(tab_schema,table_name)
    else:
        table_name = tab_info
        tab_schema = 'EDW_IT_'+table_name[:1]
        print(tab_schema,table_name)
        create_tab(tab_schema,table_name)


def merge_sql(filePath):
    out_file = '/home/use/elk_prog/table/merge_f_m_g_sql/'
    if os.path.isdir(out_file):
        print('filepath is exists')
    else:
        os.makedirs(out_file)
    cat1 = 'cat '+filePath +'sp_*.sql > ' + out_file + 'create_sp_f_m_g.sql'
    cat2 = 'cat '+filePath +'[FMG]*.sql >' +  out_file + 'create_f_m_g.sql'
    subprocess.call(cat1,shell=True)
    subprocess.call(cat2,shell=True)

if __name__=='__main__':
    get_param()
    get_cre_tab()
    #merge_sql(s)
