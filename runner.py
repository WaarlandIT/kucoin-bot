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
    my_price = my_data['price']

    my_val = (my_coin, my_current_time, my_price)
    mycursor.execute(my_sql, my_val)

  mydb.commit()
  sleep(60 / len(my_array))
