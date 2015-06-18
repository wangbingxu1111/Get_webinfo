#-*-coding:utf-8-*-
import urllib2
import re
import os
from time import strftime, localtime
import time
from bs4 import BeautifulSoup 
import shutil  


def getpic(url,content,lists):
    os.mkdir("/tmp/backup"+lists+"/images")
    soup = BeautifulSoup(content)  
    imgs = soup.findAll('img')

    img_pat = re.compile('.*/(.*)\.[jpg|gif|png]')  
 
    for img in imgs:  
        imgNames = re.findall(r'.*/(.*)\.[jpg|gif|png]',str(img))

        imgType = re.findall(r'.*/.*\.([^ ]*)"',str(img))  
        imgUrls = re.findall(r'.*src=\"([^\"]*)\"',str(img))
        if imgNames and imgType and imgUrls:
       
            imagecontent = urllib2.urlopen(imgUrls[0]).read() 
            imageName = imgNames[0]+"."+imgType[0]    
            
            with open(imageName,'wb') as code:
                code.write(imagecontent)
                code.close()
            shutil.move(imageName,"/tmp/backup"+lists+"/images")


def getcss(url,content,lists):
    os.mkdir("/tmp/backup"+lists+"/css")
    soup = BeautifulSoup(content,from_encoding="utf-8")  
    csss = soup.findAll('link',attrs={'type':'text/css'})  

    for css in csss:
        cssnames = re.findall(r'.*/(.*)\.css',str(css)) 
        cssurls = re.findall(r'.*href=\"([^\"]*)\"',str(css))  

        if cssnames: 
            csscontent = urllib2.urlopen(cssurls[0]).read() 
            cssName = cssnames[0]+".css"     
            
            with open(cssName,'wb') as code:
                code.write(csscontent)
                code.close()
            shutil.move(cssName,"/tep/backup"+lists+"/css")
                


def getjs(url,content,lists):
    os.mkdir("/tmp/backup"+lists+"/js")
    soup = BeautifulSoup(content,from_encoding="utf-8")  
    jss = soup.findAll('script',attrs={'type':'text/javascript'})  
    for js in jss:
        jsnames = re.findall(r'.*/(.*)\.js',str(js)) 
        jsurls = re.findall(r'.*src=\"([^\"]*)\"',str(js))  

        if jsnames and jsurls:  
            jscontent = urllib2.urlopen(jsurls[0]).read() 
            jsName = jsnames[0]+".js"      
            with open(jsName,'w+') as code:
                code.write(jscontent)
                code.close()
            shutil.move(jsName,"/tmp/backup"+lists+"/js")

def gethtml(url,content,lists):
  #  html_name = index.html
    
    fp = open('index.html',"w+")
    fp.write(content)
    fp.close()
    shutil.move('index.html','/tep/backup'+lists)


             
year = strftime("%Y",localtime()) 
mon  = strftime("%m",localtime()) 
day  = strftime("%d",localtime()) 
hour = strftime("%H",localtime()) 
mins  = strftime("%M",localtime())

while True:
    print year+mon+day+hour+mins
    lists = year+mon+day+hour+mins 
    os.mkdir('/tmp/backup/'+lists)
  #  time.sleep(60)
    url = 'http://m.sohu.com'
    content  = urllib2.urlopen(url).read()
    gethtml(url,content,lists)
    getjs(url,content,lists)
    getcss(url,content,lists)
    getpic(url,content,lists)
