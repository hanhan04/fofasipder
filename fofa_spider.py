import requests
import config
from lxml import etree  
import argparse
import sys
import base64
from urllib.parse import quote
import time
import os

proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'https://127.0.0.1:8080'
}

def checkconfig():
    try:
        testurl = "https://fofa.info/result?qbase64=dGl0bGU9IllvbnlvdSBOQyIgJiYgY291bnRyeT0iTVki&page=1&page_size=10"
        respond = requests.get(url = testurl,headers= config.headers)
        rep_to_html = etree.HTML(respond.text)
        urllist = rep_to_html.xpath("//span[@class=\"hsxa-host\"]/a/@href")
    except Exception as e:
        print("ERROR:" + e)
    
    if(len(urllist)):
        print("配置文件检测完成，开始初始化参数！！")
    else:
        print("config配置文件错误!!")
        sys.exit()  

def spider():
    urllist = []
    Search_key_base64 = quote(str(base64.b64encode(config.SearchKEY.encode()),encoding='utf-8'))
    for i in range(config.StartPage,config.StopPage+1):
        searchurl = "https://fofa.info/result?qbase64=" + Search_key_base64 + "&page=" + str(i) + "&page_size=10"
        respond = requests.get(url = searchurl,headers= config.headers)
        rep_to_html = etree.HTML(respond.text)

        if(len(rep_to_html.xpath("//span[@class=\"hsxa-host\"]/a/@href"))):
            urllist += rep_to_html.xpath("//span[@class=\"hsxa-host\"]/a/@href")
        else:
            break

        print("第" + str(i) + "页爬取完成")
        time.sleep(config.TimeSleep)

    print('-'*5 + '+'*10 + '-'*5)
    print("爬取完成，爬取页数总计为" + str(i))
    print("爬取数据量为" + str(len(urllist)))

    return urllist

#文件写入
def write_content(urllist,filename):
    filename = filename + ".txt"
    try:
        with open(filename,'w') as f:
            for i in range(0,len(urllist)):
                f.write(urllist[i]+ "\n")
        f.close

        print('-'*5 + '+'*10 + '-'*5)
        print("数据已存入文件" + os.getcwd() + "\\" + filename)

    except Exception as e:
        print("文件写入错误!! ERROR:" + str(e))

    

#初始化config.py中的参数
def init():

    parse = argparse.ArgumentParser(description="fofa sipder by 我只是好色")
    parse.add_argument('-sta',type=int,help='Number of pages to start crawling,the default value is 1',nargs="?",const=1,default=1,dest="StartPage")
    parse.add_argument('-sto',type=int,help='Number of pages to stop crawl,the default value is 6',nargs="?",const=6,default=6,dest="StopPage")
    parse.add_argument('-k',type=str,help='key word is searched',required="true",dest="SearchKEY")
    parse.add_argument('-t',type=str,help='Delay time,the default value is 5',nargs="?",const=3,default=3,dest="Timesleep")
    parse.add_argument('-fn',type=str,help="Set filename",nargs="?",const=time.strftime('%Y_%m_%d_%H%M%S',time.localtime(time.time())),default=time.strftime('%Y_%m_%d_%H%M%S',time.localtime(time.time())),dest="FileName")
    
    args = parse.parse_args()
    config.StartPage = args.StartPage
    config.StopPage = args.StopPage
    config.SearchKEY = args.SearchKEY
    config.TimeSleep = args.Timesleep
    config.FileName = args.FileName
    
    print(config.SearchKEY)
    print("初始化完成开始爬取")
    print('-'*5 + '+'*10 + '-'*5)
    return

def main():
    checkconfig()
    init()
    urllist = spider()
    write_content(urllist,config.FileName)


if __name__ == '__main__':
    main()