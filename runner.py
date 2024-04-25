#!/usr/bin/python3
import sys
import pandas as pd
import yaml
import mysql.connector
import time

from kucoin.client import Market
from time import sleep

my_config = '/opt/kucoin-bot/runner.yml'
m_client = Market(url='https://api.kucoin.com')

with open(my_config, 'r') as file:
    my_doc = yaml.safe_load(file)

mydb = mysql.connector.connect (
  host = my_doc['mysql']['host'],
  user = my_doc['mysql']['user'],
  password = my_doc['mysql']['pass'],
  database = my_doc['mysql']['database']
)

mycursor = mydb.cursor()

my_sql = "INSERT INTO coins (coin, time, price) VALUES (%s, %s, %s)"

my_array = my_doc['coins']
while True:
  for my_coin in my_array:
    my_ucoin = my_coin.upper()
    my_data = m_client.get_ticker(my_ucoin + '-USDT')
    my_current_time = int(time.time())
    try:
       my_old_price = my_doc['coins'][my_coin]['price']
    except Exception as e:
       my_old_price = 1
       pass
    my_price = my_data['price']
    percent = round((((float(my_data['price']) - float(my_old_price)) * 100) / float(my_old_price)),2)
    my_doc['coins'][my_coin]['price'] = my_price
    my_doc['coins'][my_coin]['lastpercent'] = percent

    with open(my_config, 'w') as sfile:
        yaml.dump(my_doc, sfile)
    my_val = (my_coin, my_current_time, my_price)
  
    mycursor.execute(my_sql, my_val)
    mydb.commit()
    
    my_start_time = int(my_current_time) - 900
    my_select = 'SELECT coin, price FROM coins where coin = %s AND time > %s order by time;'

    mycursor.execute(my_select, (my_coin, my_start_time))

    my_result = mycursor.fetchall()
    
#    print(my_ucoin)
    for x in my_result:
      my_sql_array = x
      my_calc_price = my_sql_array[1]
#      print(my_calc_price)

  sleep(60 / len(my_array))
