#/usr/bin/python
#encoding=utf-8
'''
author="heathu"
time=20180411
#敏感词文本文件 filtered_words.txt，里面的内容 和 0011题一样，当用户输入敏感词语，则用 星号 * 替换，例如当用户输入「北京是个好城市」，则变成「**是个好城市」。
'''

import sys

def get_word(file):
    words = []
    with open(file,'r') as fr:
        for line in fr:
            line = line.strip()
            words.append(line)
    return words

def replace_str(char,words):
    for x in words:
        if x in char:
            char = char.replace(x,'*'*len(x))
    print(char)
    

if __name__=="__main__":
    file = './mingan.txt'
    char = input(">")
    words = get_word(file)
    replace_str(char,words)
