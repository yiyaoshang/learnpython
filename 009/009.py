#/usr/bin/python
#encoding=utf-8
'''
#author="heathu"
#time=20180411
#**一个HTML文件，找出里面的**链接**
'''
import re
import requests
from bs4 import BeautifulSoup as bs

def get_url(url):
    content = requests.get(url).content
    soup = bs(content,'html.parser')
    links = soup.findAll('a')
    for link in links:
        print(link['href'])

if __name__=="__main__":
    url = "https://www.nowcoder.com"
    get_url(url)
