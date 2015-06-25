#coding=utf-8
import urllib2
import re
import os
from time import strftime, localtime
import time
from bs4 import BeautifulSoup 
import shutil  
import sys,getopt

#获取图像文件
def getpic(url,lists):
    content  = urllib2.urlopen(url).read()
    os.makedirs(con+"/"+lists+"/images")
    soup = BeautifulSoup(content)  
    imgs = soup.findAll('img')

    img_pat = re.compile('.*/(.*)\.[jpg|gif|png]')  
 
    for img in imgs:  
        imgNames = re.findall(r'.*/(.*)\.[jpg|gif|png]',str(img))

        imgType = re.findall(r'.*/.*\.([^ ]*)"',str(img))  
        imgUrls = re.findall(r'.*src=\"([^\"]*)\"',str(img))
        if imgNames and imgType and imgUrls:
       
            imagecontent = urllib2.urlopen(imgUrls[0]).read() #读进image数据
            imageName = imgNames[0]+"."+imgType[0]    #image文件的名字
            print imageName
            filename =con+ "/"+lists+"/images/"+imageName
         #   print filename
            if os.path.exists(filename): 
                print ""
            else:
                with open(imageName,'wb') as code:
                    code.write(imagecontent)
                    code.close()
                shutil.move(imageName,con+"/"+lists+"/images")

#获取css文件
def getcss(url,lists):
    content  = urllib2.urlopen(url).read()
    os.makedirs(con+"/"+lists+"/css")
    soup = BeautifulSoup(content,from_encoding="utf-8")  
    csss = soup.findAll('link',attrs={'type':'text/css'})  

    for css in csss:
        cssnames = re.findall(r'.*/(.*)\.css',str(css)) 
        cssurls = re.findall(r'.*href=\"([^\"]*)\"',str(css))  

        if cssnames: 
            csscontent = urllib2.urlopen(cssurls[0]).read() #读进css数据
            cssName = cssnames[0]+".css"      #css文件的名字
            
            with open(cssName,'wb') as code:
                code.write(csscontent)
                code.close()
            shutil.move(cssName,con+"/"+lists+"/css")
                

#获取js文件
def getjs(url,lists):
    content  = urllib2.urlopen(url).read()
    os.makedirs("/tmp/backup/"+lists+"/js")
    soup = BeautifulSoup(content,from_encoding="utf-8")  
    jss = soup.findAll('script',attrs={'type':'text/javascript'})  #找出含有type="text/javascript"特性的 
    for js in jss:
        jsnames = re.findall(r'.*/(.*)\.js',str(js)) 
        jsurls = re.findall(r'.*src=\"([^\"]*)\"',str(js))  

        if jsnames and jsurls:  
            jscontent = urllib2.urlopen(jsurls[0]).read() #读进js数据
            jsName = jsnames[0]+".js"      #js文件的名字
            with open(jsName,'w+') as code:
                code.write(jscontent)
                code.close()
            shutil.move(jsName,con+"/"+lists+"/js")

#获取index.html文件
def gethtml(url,lists):
    content  = urllib2.urlopen(url).read()
    fp = open('index.html',"w+")
    fp.write(content)
    fp.close()
    shutil.move('index.html',con+'/'+lists)


#获取系统时间信息
option,long = getopt.getopt(sys.argv[1:],"hd:u:o:")
for key,value in option:
    if key in ("-d"):
        get_time = int(value)
    if key in ("-u"):
        get_url = value
    if key in ("-o"):
        con = value
print get_time
print get_url
print con
while True:
    year = strftime("%Y",localtime()) 
    mon  = strftime("%m",localtime()) 
    day  = strftime("%d",localtime()) 
    hour = strftime("%H",localtime()) 
    mins  = strftime("%M",localtime())


#   print year+mon+day+hour+mins
    lists = year+mon+day+hour+mins
    os.makedirs(con+"/"+lists)

    
    url = get_url
    
    content  = urllib2.urlopen(url).read()
    gethtml(url,lists)
    getjs(url,lists)
    getcss(url,lists)
    getpic(url,lists)
    time.sleep(get_time)
