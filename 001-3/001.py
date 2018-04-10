#/usr/bin/python
#encoding=utf-8
'''
author="heathu"
date=20180410
做为 Apple Store App 独立开发者，你要搞限时促销，为你的应用生成激活码（或者优惠券），使用 Python 如何生成 200 个激活码（或者优惠券）
'''
import uuid

def gen_coupon(num):
    coupon_id = []
    for i in range(num):
        cid = str(uuid.uuid4())
        coupon_id.append(cid)
    return coupon_id

if __name__=="__main__":
    num = 200
    couid = gen_coupon(num)
    print couid
