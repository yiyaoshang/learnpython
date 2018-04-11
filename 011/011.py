#/usr/bin/python
#encoding=utf-8
'''
author="heathu"
time=20180411
# 敏感词文本文件 filtered_words.txt，里面的内容为以下内容，当用户输入敏感词语时，则打印出 Freedom，否则打印出 Human Rights。
'''
import sys
import jieba

def get_word(file):
    words = []
    with open(file,'r') as fr:
        for line in fr:
            line = line.strip()
            words.append(line)
    return words

def check_print(char,words):
    seg = jieba.cut(char)
    s = ",".join(seg)
    n = s.count(',')+1
    count = 0
    for i in range(n):
        c = s.split(',')[i]
        if c in words:
            count += 1
    if count == 0:
        print("Human Rights")
    else:
        print("Freedom")
            
    

if __name__=="__main__":
    file = './mingan.txt'
    char = input(">")
    words = get_word(file)
    check_print(char,words)
