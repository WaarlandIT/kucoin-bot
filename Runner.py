#!/usr/bin/python3
import sys
import pandas as pd
import yaml
import mysql.connector

from kucoin.client import Market

my_config = '/opt/kucoin-bot/runner.yml'
m_client = Market(url='https://api.kucoin.com')

with open(my_config, 'r') as file:
    my_doc = yaml.safe_load(file)

my_coin = 'BTC'

my_data = m_client.get_ticker(my_coin + '-USDT')

mydb = mysql.connector.connect (
  host = my_doc['mysql']['host'],
  user = my_doc['mysql']['user'],
  password = my_doc['mysql']['pass'],
  database = my_doc['mysql']['database']
)

print(my_data)
