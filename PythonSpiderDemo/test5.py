# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import datetime
import time

success = False
flag = False
data = ""


def request():
    headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection': 'Keep-Alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
    response = requests.get(
        "https://www.hibbett.com/jordan-1-mid-white-metallic-black-mens-shoe/Q0405.html?dwvar_Q0405_color=0171&cgid=Brands#start=4",
        headers=headers)
    return response


def parse(response):
    soup = BeautifulSoup(response.content, "lxml")
    result = soup.select(
        ".pt_product-details #main #primary #pdpMain #product-content .product-variations .size .value .swatches .selectable .swatchanchor")
    print "现在有的尺寸,请求时间" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    global data, flag, success
    temp = ""
    for item in result:
        print item.text.replace("\n", "").replace("size", "") + " ",
        temp += item.text.replace("\n", "").replace("size", "") + " "
    if not flag:
        data = temp
        flag = True
    else:
        if data == temp:
            pass
        else:
            success = True
    print "\n"


if __name__ == '__main__':
    while True:
        if not success:
            parse(request())
            time.sleep(60)
        else:
            print "\n库存变动！！！"
            time.sleep(60)
