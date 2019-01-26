# -*- coding: utf-8 -*-

# 用来抓取每日优鲜指定sku的近期销量

fpath = '/var/www/html/missfresh/'
sku_list = [
            "p-hbxjkelxl-5g", "p-hbkel-10g",
            "p-sghg-70g-100g",
            "p-HBdjhmj-1h",
            "p-hbytxfq-500g",
            "p-hbgnqc11-2g",
            "p-hbzjcm-1h",
            "p-hdsghycm-1h", "p-HNhycmsd-1h",
            "p-hb-hycm350g1h", "p-hdhycm350g-1h",
            "p-hb-ynppg-250gyh",
            "p-hdstj-1j",
            "p-hbqxsng-yzl-1h"
            ]
address_code = '110106'
station_code = 'MRYX|mryx_jgmpx'
detail_url = 'https://as-vip.missfresh.cn/v3/product/'
headers = {
    "version":"4.5.1.0.2",
    "x-region":'{"station_code":"'+ station_code +'","address_code":'+ address_code +'}',
    "user-agent":"Mozilla/5.0 (Linux, Android 6.0, Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36",
    "accept-language":"zh-CN,zh,q=0.9,en,q=0.8",
    "accept":"application/json, text/plain, */*",
    "authority":"as-vip.missfresh.cn",
    "scheme":"https",
    "platform":"web",
    "method":"GET"
    }


import requests
import openpyxl
from datetime import date
from time import sleep
from random import random

result = []

for sku in sku_list:
   r = requests.get(detail_url + sku, headers=headers)
   if r.status_code == 200:
       if 'msg' in r.json():
           result.append([date.today() , sku, '-', '-', r.json()['msg']])
           pass
       else:
           result.append([date.today() , sku, r.json()['name'], int(r.json()['sales_volume']), int(r.json()['vip_price_pro']['price_down']['price'])/100])
   sleep( random() * 5 )
#print (result)

try:
    wb = openpyxl.load_workbook(fpath + 'sale_volume.xlsx')
    ws = wb.active
except FileNotFoundError:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['日期','sku','品名','销量',"价格"])


for row in result:
    ws.append(row)
    
wb.save(fpath + 'sale_volume.xlsx')

