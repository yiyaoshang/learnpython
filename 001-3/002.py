#/usr/bin/python
#encoding=utf-8
'''
author="heathu"
date=20180410
做为 Apple Store App 独立开发者，你要搞限时促销，为你的应用生成激活码（或者优惠券），使用 Python 如何生成 200 个激活码（或者优惠券）
将优惠卷存入mysql数据库
'''
import uuid
import pymysql

def gen_coupon(num):
    coupon_id = []
    for i in range(num):
        cid = str(uuid.uuid4())
        coupon_id.append(cid)
    return coupon_id

def conn_db():    
    conn = pymysql.connect(user='test_01',password='test_01',host='114.55.84.146',db='test',charset='utf8')
    return conn

def store_db():
    couponid = gen_coupon(200)
    conn = conn_db()
    cursor = conn.cursor()
    drop_sql = 'drop table if exists coupon'
    create_sql = 'create table coupon(id int auto_increment primary key,couponid varchar(50))'
    insert_sql = 'insert into coupon(couponid) values(%s)'
    cursor.execute(drop_sql)
    cursor.execute(create_sql)
    cursor.executemany(insert_sql,couponid)
    conn.commit()
    
    
if __name__=="__main__":
    store_db()
