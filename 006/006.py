#/usr/bin/python3.5
#encoding=utf-8
'''
author="heathu"
time=20180411
#  你有一个目录，放了你一个月的日记，都是 txt，为了避免分词的问题，假设内容都是英文，请统计出你认为每篇日记最重要的词。
'''
import re
from collections import Counter
import os

def create_list(file):
    fr = open(file,'r')
    datalist = []
    for line in fr:
        line = line.strip()
        content = re.sub('\"|,|\.','',line)
        datalist.extend(content.strip().split(' '))
    return datalist

def wc_top_k(datalist):
    c =  Counter(datalist)
    s = c.most_common(1)
    return s

def path_walk(path):
    f_list = []
    for root,dirs,files in os.walk(path):
        for file in files:
            file = os.path.join(root,file)
            f_list.append(file)
    return f_list

if __name__=="__main__":
    path = './test/'
    f_list = path_walk(path)
    for f in f_list:
        data = create_list(f)
        s = wc_top_k(data)
        fname = f.split("/")[-1]
        print fname,s
    
