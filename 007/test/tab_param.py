#!/usr/bin/env python
# coding:utf8

__author="heathu"

import pandas as pd 
import os
import sqlite3
import config

def combination(names):
    return ','.join(names)

def get_dfs():
    dfs=pd.read_excel(excel,sheetname=sheets,skiprows=1,keep_default_na=False,index_col=False,header=0)
    return dfs

def get_tab_com(dfs):
    df=dfs[num].sort_values(by=['tab_name','col_seq'],ascending=True)
    df['col_info']=df['col_name']+' '+df['col_type']
    df['col_num']="'{}'"
    tab=df[['tab_name','col_info','col_num']]
    tab_com=tab.groupby('tab_name').aggregate(combination)
    sht=df[['tab_name','sheet_seq']]
    #按tab_name,sheet_seq去重
    sht=sht.drop_duplicates()
    #将索引tab_name变成列
    tab_com =tab_com.reset_index()
    #对tab_com和sht按照tab_name进行内关联
    tab_com=pd.merge(tab_com, sht, on = ['tab_name'], how = 'inner')
    return tab_com

def get_sql(dfs,tab_com):
    for indexs in tab_com.index:
        sheet_seq=tab_com.loc[indexs,'sheet_seq']
        tab_name=tab_com.loc[indexs,'tab_name']
        col_info=tab_com.loc[indexs,'col_info']
        col_num=tab_com.loc[indexs,'col_num']
        drop_sql = 'drop table if exists {};\n'.format(tab_name)
        cre_sql  = 'create table {}({});\n'.format(tab_name,col_info)
        ins_sql  = 'insert into {} values({});\n'.format(tab_name,col_num)
        col_nums = dfs[sheet_seq].values.tolist()
        with open(config.SqlPath+config.sep+tab_name+'.sql', 'w',encoding="utf-8") as file_object:
            file_object.write(drop_sql)
            file_object.write(cre_sql)
            for col_num in col_nums:
                col_num = [str(i) for i in col_num]
                insert_sql = ins_sql.format(*col_num)
                file_object.write(insert_sql)
        cur.execute(drop_sql)
        cur.execute(cre_sql)
        cur.executemany(ins_sql.replace("'{}'","?"),col_nums)
        print("Insert {} {}  rows!".format(tab_name,str(cur.rowcount)))
    conn.commit()
    cur.close()
    conn.close()


def get_param(excels):
    global path,excel,sheets,num,conn,cur
    path = config.ExcelPath
    excel = excels[0]
    sheets = excels[1]
    num = excels[2]
    conn=config.con_DB()
    cur=conn.cursor()
    os.chdir(path)
    print('work_directory: ', os.getcwd())

if __name__=="__main__":
    excellist = [['F_M_G_PARAM.xlsx',[2,3,4,5,6,7,8],8],['O_S_PARAM.xlsx',[3,4,5],5]]
    for excels in excellist:
        get_param(excels)
        dfs = get_dfs()
        tab_com = get_tab_com(dfs)
        get_sql(dfs,tab_com)