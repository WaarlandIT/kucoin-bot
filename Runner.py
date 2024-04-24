#!/usr/bin/python3
import sys
import pandas as pd
import yaml
import mysql.connector

from kucoin.client import Market

my_config = '/opt/kucoin-bot/runner.yml'
m_client = Market(url='https://api.kucoin.com')

my_coin = 'BTC'

my_data = m_client.get_ticker(my_coin + '-USDT')

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="mydatabase"
)

print(my_data)
