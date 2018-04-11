#/usr/bin/python
#encoding=utf-8
'''
author="heathu"
time=20180411
#**使用 Python 生成类似于下图中的**字母验证码图片**
'''
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random
import string

def randcor():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def randchar():
    s =  [random.choice(string.ascii_uppercase) for i in range(4)]
    char = ''.join(s)
    return char

def gen_img():
    char = randchar()
    size = (400,100)
    img = Image.new('RGB',size,color=0)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('abc.ttf',size=80)
    total = 0
    for x in range(400):
        for y in range(100):
            col = img.getpixel((x,y))
            draw.point((x,y),fill=randcor())
    for i in range(4):
        draw.text((80+400*i*0.2,20),char[i],font=font,fill=randcor())
    img = img.filter(ImageFilter.BLUR)
    img.save('result.jpg','jpeg')

if __name__=="__main__":
    gen_img()
