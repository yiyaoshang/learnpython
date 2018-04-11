#/usr/bin/python3.5
#encoding=utf-8
'''
author="heathu"
time=20180410
#  *任一个英文的纯文本文件，统计其中的单词出现的个数
'''
import re
from collections import Counter

def create_list(file):
    fr = open(file,'r')
    datalist = []
    for line in fr:
        line = line.strip()
        content = re.sub('\"|,|\.','',line)
        datalist.extend(content.strip().split(' '))
    return datalist

def wc(datalist):
    c = Counter(datalist)
    return c

if __name__=="__main__":
    file = "./test.txt"
    datalist = create_list(file)
    c = wc(datalist)
    print c
