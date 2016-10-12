# coding=gbk

from bs4 import BeautifulSoup
import urllib2,urllib
import cookielib
import gzip,cStringIO
import sys
import time
import datetime
import re

baseUrl = 'https://bbs.sjtu.cn/'

class Post(object):
    Url = ''
    Author = ''
    Title = ''
    Time = ''
    Content = ''
    

def constructPageUrl(board,page):
    return 'https://bbs.sjtu.cn/bbstdoc?board=' + board + '&page=' + page

def postsOfPage(pageUrl):
    postsurl = {}
    boardPage = urllib2.urlopen(pageUrl).read().decode('gbk', 'ignore')
    soup = BeautifulSoup(boardPage)
    content = soup.find_all('a', href=True)
    for tag in content:
        if 'reid' in tag['href']:
            postsurl[baseUrl + tag['href']] = unicode(tag.string[2:])
            #postsurl.append(baseUrl + tag['href'])
    return postsurl

def parsePost(posturl):
    postPage = urllib2.urlopen(posturl).read().decode('gbk', 'ignore')
    textLines = postPage.split('\n')
    post = Post()    
    post.Url = posturl
    contentNow = False
    for line in textLines:
        if (len(post.Author)==0) and (u'发信人' in line):
            post.Author = line[line.index(u'发信人')+5:line.index(',')]    
        if (len(post.Title)==0) and (u'标  题:' in line):
            post.Title = line[line.index(u'标  题:')+5:]
        if (len(post.Time)==0) and (u'发信站:' in line):
            post.Time = line[line.index(u'(')+1:line.index(u')')]
            contentNow = True
            continue
        if contentNow:
            if u'※ 来源' in line:
                return post
            else:                
                post.Content = post.Content + line + '\n'

board = 'Modern_Poem'
page = 1

pageurl = constructPageUrl(board,str(page))
allposts = postsOfPage(pageurl)
for posturl in allposts.keys():
    currPost = parsePost(posturl)
    print allposts[posturl]

