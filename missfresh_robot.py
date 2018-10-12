# -*- coding: utf-8 -*-

# 用来抓取每日优鲜指定sku的近期销量

fpath = '/var/www/html/missfresh/'
sku_list = ['p-hbqxspdt-4g', 'p-tjspt-2g', 'p-hbspdt-2g',
            'p-hbnmxss-1h', 'p-tjnmxsz-1h',
            'p-hbjhxpg-1d',
            "p-hbngl-5g", "p-tjngl-5g",
            "p-hbcts-2g", "p-tjyncts-2g",
            "p-hbjfpt-1h", "p-tjjfpt-1h",
            "p-hbxjkelxl-5g", "p-hbkel-10g",
            "p-hbdldz1j-1h-new", "p-tjdldz1j-2h",
            "p-HBlbxg-2g",
            "p-hbhhdzx-1h",
            "p-hbfptxs-2g",
            "p-HBzhdz-1h",
            "p-hbytxfq-500g-new", "p-hbytxfq-500g",
            "p-sghg-70g-100g",
            "p-hbqylx-2g",
            "p-HBdjhmj-1h",
            "p-hbay38-2g",
            "p-hbjqhmt-2g",
            "p-sghg-70g-100g",
            "p-hbytxfq-500g", "p-hbytxfq-500g-new",
            "p-hbxjxafpg-1h"
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
    wb = openpyxl.load_workbook(fpath + 'data.xlsx')
    ws = wb.active
except FileNotFoundError:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['日期','sku','品名','销量',"价格"])


for row in result:
    ws.append(row)
    
wb.save(fpath + 'data.xlsx')
        
