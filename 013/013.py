#/usr/bin/python
#encoding=utf-8
'''
author="heathu"
time=20180411
#** 用 Python 写一个爬图片的程序，爬 [这个链接里的日本妹子图片 :-)](http://tieba.baidu.com/p/2166231880)
'''
import requests
import re
from bs4 import BeautifulSoup as bs

def get_img(url):
    img_urls = []
    content = requests.get(url).content
    soup = bs(content,'html.parser')
    imgs = soup.find_all('img',{'class':'BDE_Image'})
    for img in imgs:
        img_urls.append(img['src'])
    return img_urls

def down_img(url):
    content = requests.get(url).content
    with open(url[-16:-6]+'.jpg','ab') as fw:
        fw.write(content)

if __name__=="__main__":
    url = 'http://tieba.baidu.com/p/2166231880'
    img_urls = get_img(url)
    for img_url in img_urls:
        down_img(img_url)
