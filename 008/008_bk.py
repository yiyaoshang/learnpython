#!/usr/bin/env python
#coding: utf-8
from goose import Goose
from goose.text import StopWordsChinese
url = 'http://www.ruanyifeng.com/blog/2015/05/thunk.html'
def extract(url):
    g = Goose({'stopwords_class': StopWordsChinese})
    article = g.extract(url=url)
    return article.cleaned_text
if __name__ == '__main__':
    print extract(url)
