# coding=gbk

from bs4 import BeautifulSoup
import urllib2,urllib
import cookielib
import gzip,cStringIO
import sys
import time
import datetime
import re

urlbase = 'https://bbs.sjtu.edu.cn/bbsdoc?board='
urlPostBase = 'https://bbs.sjtu.edu.cn/bbstdoc,board,'

board = 'book'

def getNewPosts(Time, Board):
    #url = urlPostBase + board + '.html'
    url = urlbase + board
    boardPage = urllib2.urlopen(url).read().decode('gbk', 'ignore')

    soup = BeautifulSoup(boardPage)
    
    content = soup.find_all('a', href=True)

    for tag in content:
        tagstring = unicode(tag.string)
    
    return 0;

result = getNewPosts(0,board);
