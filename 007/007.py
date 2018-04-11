#/usr/bin/python3.5
#encoding=utf-8
'''
author="heathu"
time=20180411
#  *有个目录，里面是你自己写过的程序，统计一下你写过多少行代码。包括空行和注释，但是要分别列出来。
'''
import re
import os

def stat_lines(file):
    fr = open(file,'r')
    pattern = '[(#)(//)(/*)(*)]'
    stat = [0,0,0]
    for line in fr:
        line = line.strip()
        if len(line) == 0:
            stat[0] += 1
        elif "#" in line:
            stat[1] += 1
        else:
            stat[2] += 1
    return stat

def path_walk(path):
    f_list = []
    for root,dirs,files in os.walk(path):
        for file in files:
            f_path = os.path.join(root,file)
            f_list.append(f_path)
    return f_list


if __name__=="__main__":
    path = './test/'
    f_list = path_walk(path)
    s = [0,0,0] 
    for f in f_list:
        stat = stat_lines(f)
        s = [s[i]+stat[i] for i in range(3)]
    print s


