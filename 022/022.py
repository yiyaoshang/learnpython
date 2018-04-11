#encoding=utf-8

"""
author="heathu"
date=20180410
#iPhone 6、iPhone 6 Plus 早已上市开卖。请查看你写得 第 0005 题的代码是否可以复用。
"""
import os
from PIL import Image

PHONE = {'iPhone5':(1136,640), 'iPhone6':(1134,750), 'iPhone6P':(2208,1242)}

def resize_pic(path,new_path,phone_type):
    img = Image.open(path)
    w,h = img.size
    width,height = PHONE[phone_type]
    if w > width:
        w = width
        h = w * height // h
    if h > height:
        h = height
        w = h * width // w
    new_img = img.resize((w,h),Image.ANTIALIAS)
    new_img.save(new_path)

def walk_dir(path,phonetype):
    for root,dirs,files in os.walk(path):
        for f_name in files:
            if f_name.lower().endswith('jpg'):
                path_dst = os.path.join(root,f_name)
                f_new_name = phonetype + f_name
                resize_pic(path_dst, f_new_name,phonetype)

if __name__=="__main__":
    walk_dir('./','iPhone6')
