#encoding=utf-8
import subprocess
import config as cg
import sys
import cre_fgm_tab as cfgm
import cre_ft_tab as cft
import cre_os_tab as cos
import db_cre_tab as db
import make_data_file as mk_fl

def get_input():
    print('输入上传文件日期 YYYYMMDD')
    date = input()
    return date

def execute(date,type):
    if type == 'oracle':
        path =  "@/home/use/"+date+"/upload/know.sql"
        cmd1 = "sqlplus "+cg.dbuser+"/"+cg.dbpasswd+"@"+cg.dbsid+" "+path
    elif type == 'pg':
        path =  "/home/use/"+date+"/upload/init.sql"
        cmd1 = "gsql -U "+cg.user+" -W "+cg.passwd+" -d jcfcedw -p 25108 -h "+cg.dbip+" -f "+path
    subprocess.call(cmd1,shell=True)

def __init__(date,type):
    if type == "1":
        print("知识库建表")
        execute(date,'oracle')
    elif type == "2":
        print("ELK数据库初始化")
        print("启动GDS服务")
        gdscmd = "sh /home/use/elk_prog/app/gds_restart.sh "+date
        subprocess.call(gdscmd,shell=True)
        print("上传码值表 生命周期表 万能日历表文件")
        mkcmd = "mkdir -p /data/edwdata/input/"+date
        cpcmd = "cp /home/use/"+date+"/upload/*.txt /data/edwdata/input/"+date+"/"
        subprocess.call(mkcmd,shell=True)
        subprocess.call(cpcmd,shell=True)
        print("插入码值表，生命周期表，万能日历表")
        sedcmd = "sed -i 's/scip_127.0.0.1_scip/"+cg.ft_in_ip+"/g' /home/use/"+date+"/upload/init.sql"
        subprocess.call(sedcmd,shell=True)
        execute(date,'pg')
    

def create_tab_pro(date,type,tablename=""):
    path1 = cfgm.begin()
    path2 = cft.get_cre_tab()
    path3 = cos.get_cre_tab()
    path4 = "/home/use/"+date+"/upload/manul"
    print(path1,path2,path3,path4)
    if type == "1":
        db.db_cre(path1)
        db.db_cre(path2)
        db.db_cre(path3)
        db.db_cre(path4)
        print("init_sql successful")
    elif type == "2":
        path5 = "/home/use/elk_prog/table/create_tab/etl/tmp_sql"
        cpcmd = "cp "+path1+"/*"+tablename+".sql "+path5
        cpcmd2 = "cp "+path2+"/FT_"+tablename+".sql "+path5
        subprocess.call(cpcmd2,shell=True)
        subprocess.call(cpcmd,shell=True)
        #db.db_cre(path5)
        print("init_sql successful")

def make_file():
    mk_fl.main()

def main():
    cos.get_param()
    cfgm.get_param()
    cft.get_param()
    cfgm.get_cre_tab()
    cft.get_cre_tab()
    cos.get_cre_tab()

if __name__=='__main__':
    #date = get_input()
    date = sys.argv[1]
    #tablename = sys.argv[2]
    #__init__(date,"1")
    #__init__(date,"2")
    #create_tab_pro(date,"2",tablename)
    #make_file()
    main()

