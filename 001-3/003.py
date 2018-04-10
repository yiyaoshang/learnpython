#/usr/bin/python
#encoding=utf-8
'''
author="heathu"
date=20180410
做为 Apple Store App 独立开发者，你要搞限时促销，为你的应用生成激活码（或者优惠券），使用 Python 如何生成 200 个激活码（或者优惠券）
将优惠卷存入redis数据库
'''
import uuid
import redis

def gen_coupon(num):
    coupon_id = []
    for i in range(num):
        cid = str(uuid.uuid4())
        coupon_id.append(cid)
    return coupon_id

def conn_db():    
    conn = redis.Redis(host='127.0.0.1',port=6379,db=0)
    return conn

def store_db():
    couponid = gen_coupon(200)
    conn = conn_db()
    for key in couponid:
        conn.lpush('key', key)
    
    
if __name__=="__main__":
    store_db()
