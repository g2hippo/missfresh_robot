# -*- coding: utf-8 -*-

# 用来抓取每日优鲜指定sku的近期销量

fpath = '/var/www/html/missfresh/'
sku_list = ['p-hbqxspdt-4g', 'p-tjspt-2g']
address_code = '110106'
detail_url = 'https://as-vip.missfresh.cn/v3/product/'
headers = {
    "version":"4.5.1.0.2",
    "x-region":'{"address_code":'+ address_code +'}',
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
from  datetime import date

result = []

for sku in sku_list:
   r = requests.get(detail_url + sku, headers=headers)
   if r.status_code == 200:
       if 'msg' in r.json():
           #print(sku, r.json()['msg'])
           pass
       else:
           result.append([date.today() , sku, r.json()['name'], int(r.json()['sales_volume'])])

#print (result)

try:
    wb = openpyxl.load_workbook(fpath + 'data.xlsx')
    ws = wb.active
except FileNotFoundError:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['日期','sku','品名','销量'])


for row in result:
    ws.append(row)
    
wb.save(fpath + 'data.xlsx')
        
