#encoding=utf-8

"""
author="heathu"
date=20180410
第 0005 题：你有一个目录，装了很多照片，把它们的尺寸变成都不大于 iPhone5 分辨率的大小。
"""
import os
from PIL import Image

iPhone5_WIDTH = 1136
iPhone5_HEIGHT = 640

def resize_pic(path,new_path,width=iPhone5_WIDTH,height=iPhone5_HEIGHT):
    img = Image.open(path)
    w,h = img.size
    if w > width:
        w = width
        h = w * height // h
    if h > height:
        h = height
        w = h * width // w
    new_img = img.resize((w,h),Image.ANTIALIAS)
    new_img.save(new_path)

def walk_dir(path):
    for root,dirs,files in os.walk(path):
        for f_name in files:
            if f_name.lower().endswith('jpg'):
                path_dst = os.path.join(root,f_name)
                f_new_name = 'iPhone5_' + f_name
                resize_pic(path=path_dst, new_path=f_new_name)

if __name__=="__main__":
    walk_dir('./')
