# coding=gbk

from bs4 import BeautifulSoup
import urllib2,urllib
import cookielib
import gzip,cStringIO
import sys
import time
import datetime
import re
import md5
import os
import os.path

baseUrl = 'https://bbs.sjtu.cn/'
folder = 'unpublished'
if not os.path.exists(folder):
    os.makedirs(folder)

class Post(object):
    Url = ''
    Author = ''
    Title = ''
    Time = ''
    Content = ''
    WholePost = ''
    Index = 0
    

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
    textLines = BeautifulSoup(postPage).text.split('\n')
    post = Post()    
    post.Url = posturl
    contentNow = False
    recordBegin = False
    for line in textLines:        
        if (len(post.Author)==0) and (u'发信人' in line):
            post.Author = line[line.index(u'发信人')+5:line.index(',')]    
            recordBegin = True
        if (len(post.Title)==0) and (u'标  题:' in line):
            post.Title = line[line.index(u'标  题:')+5:]
        if (len(post.Time)==0) and (u'发信站:' in line):
            post.Time = line[line.index(u'(')+1:line.index(u')')]
            contentNow = True
            continue
        if(u'返回上一页' in line):
            return post
        if contentNow:
            if line == u'--':
                contentNow = False
            else:                
                post.Content = post.Content + line + '\n'
        if(recordBegin):
            post.WholePost = post.WholePost + line + '\n'


def savePostToFile(post):
    postFile = open( folder + '\\' + md5.new(post.Url).hexdigest()+'.post','w')       
    postFile.write(str(post.Index) + '\n');
    postFile.write(post.Url + '\n') 
    postFile.write(post.Title.encode('utf8') + '\n')
    postFile.write(post.Author.encode('utf8') + '\n') 
    postFile.write(post.Content.encode('utf8') + '\n')       
    postFile.write(post.Time.encode('utf8') + '\n')
    postFile.close()

board = 'Modern_Poem'
page = 1
postIndex = 0
allPostsRecord = []
recordFile = folder + '\\all_posts.dat'

if not os.path.isfile(recordFile):
    postRecord = open(folder + '\\all_posts.dat','w')
else:
    postRecord = open(folder + '\\all_posts.dat','r')
    allPostsRecord = postRecord.readlines();    
    postRecord.close();    
    postIndex = int(allPostsRecord[len(allPostsRecord)-1].split(' ')[2])
    page = postIndex/20;
    for i in range(0,len(allPostsRecord),1):
        allPostsRecord[i] = allPostsRecord[i].split(' ')[0]
    postRecord = open(recordFile,'a');

finished = False

while not finished:
    pageurl = constructPageUrl(board,str(page))    
    allposts = postsOfPage(pageurl)
    for posturl in allposts.keys():
        if posturl in allPostsRecord:
            print "already exists\n"
            continue;
        currPost = parsePost(posturl)
        currPost.Index = postIndex;
        print str(page) + ':' + allposts[posturl]
        savePostToFile(currPost)
        allPostsRecord.append(posturl)
        postRecord.write(posturl+' '+md5.new(posturl).hexdigest() + ' ' + str(postIndex) + '\n')
        postIndex = postIndex + 1
    page = page + 1

postRecord.close();
print "\n finished\n"

        
        

