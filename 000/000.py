#/usr/bin/python
#encoding=utf-8
'''
author='heathu'
time 20180410
作用：将头像的右上角添加数字
'''
from PIL import Image,ImageDraw,ImageFont

def add_num(img,num):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('ahronbd.ttf',size=100)
    color = '#FF0000'
    width,height = img.size
    draw.text((width*0.8,0),num,font=font,fill=color)
    img.save('result.jpg','jpeg')
    return 0


if __name__=="__main__":
    img = Image.open('tx2.jpg')
    num = '4'
    add_num(img,num)
