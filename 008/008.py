#/usr/bin/python3
#encoding=utf-8
'''
#author="heathu"
#time=20180411
#**第 0008 题：**一个HTML文件，找出里面的**正文**。
'''
import requests
from bs4 import BeautifulSoup as bs

def get_content(url):
    content = requests.get(url).content
    soup = bs(content,'html.parser')
    print(soup.body.text)


if __name__=="__main__":
    url = 'https://neihanshequ.com'
    get_content(url)
