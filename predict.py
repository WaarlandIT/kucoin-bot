#!/usr/bin/python3
import sys
import pandas as pd
import yaml
import mysql.connector
import time
import array

from time import sleep

my_time_frame = 900


my_config = '/opt/kucoin-bot/runner.yml'
with open(my_config, 'r') as file:
    my_doc = yaml.safe_load(file)

mydb = mysql.connector.connect (
  host = my_doc['mysql']['host'],
  user = my_doc['mysql']['user'],
  password = my_doc['mysql']['pass'],
  database = my_doc['mysql']['database']
    )

mycursor = mydb.cursor()
my_array = my_doc['coins']

for my_coin in my_array:
    my_ucoin = my_coin.upper()
    my_current_time = int(time.time())
    my_start_time = int(my_current_time) - my_time_frame
    my_select = 'SELECT coin, price FROM coins where coin = %s AND time > %s order by time;'

    mycursor.execute(my_select, (my_coin, my_start_time))
    my_result = mycursor.fetchall()
    my_calc_price0 = 0  
    my_step = 0
    for x in my_result:
        my_sql_array = x
        my_calc_priceX = my_sql_array[1]
    #    if my_step != 0:
            

        my_predict_array = array.array('d', [my_calc_priceX])
        my_calc_price0 = my_calc_priceX
        my_step +=1

print(my_predict_array)