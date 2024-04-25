#!/usr/bin/python3
import sys
import pandas as pd
import yaml
import mysql.connector
import time

from time import sleep

my_config = '/opt/kucoin-bot/runner.yml'

mydb = mysql.connector.connect (
  host = my_doc['mysql']['host'],
  user = my_doc['mysql']['user'],
  password = my_doc['mysql']['pass'],
  database = my_doc['mysql']['database']
)

mycursor = mydb.cursor()

my_array = my_doc['coins']
while True:
  for my_coin in my_array:
    my_ucoin = my_coin.upper()

    my_time_frame = 900

    my_start_time = int(my_current_time) - my_time_frame
    my_select = 'SELECT coin, price FROM coins where coin = %s AND time > %s order by time;'

    mycursor.execute(my_select, (my_coin, my_start_time))
    my_result = mycursor.fetchall()
    
    my_step = 0
    for x in my_result:
      my_sql_array = x
      my_calc_price = my_sql_array[1]
      my_insert_sql = 'INSERT INTO '
      my_step +=1
