#/usr/bin/python3.5
#encoding=utf-8
'''
author="heathu"
time=20180410
#  *任一个英文的纯文本文件，统计其中的单词出现的个数
'''
import re

def stat_word(file):
    fr = open(file,'r')
    character = []
    stat = {}
    for line in fr:
        line = line.strip()
        if len(line) == 0:
            continue
        content = re.sub('\"|,|\.','',line)
        datalist = content.strip().split(' ')
        for data in datalist:
            if not data in character:
                character.append(data)
        # 尚未记录在stat中
            if data not in stat:
                stat[data] = 0
        # 出现次数加1
            stat[data] += 1
    return stat

if __name__=="__main__":
    file = "test.txt"
    stat = stat_word(file)
    stat = sorted(list(stat.items()), key=lambda d:d[1], reverse=True)
    print(stat) 
