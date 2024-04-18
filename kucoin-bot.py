#!/usr/bin/python3
import sys
import pandas as pd
import requests
import json
import datetime
import yaml

from kucoin.client import Market
from kucoin.client import Trade
from time import sleep

my_config = 'kucoin-bot.yml'
my_logfile = 'kucoin-bot.log'


my_log = open(my_logfile, "a")
sleep(2)
my_log.write('########### \n' + format(datetime.datetime.now()) + ' Start bot \n')

with open(my_config, 'r') as file:
    my_doc = yaml.safe_load(file)

my_api_key = my_doc['api']['key']
my_api_passphrase = my_doc['api']['pass']
my_api_secret = my_doc['api']['secret']

my_array = my_doc['coins']

m_client = Market(url='https://api.kucoin.com')
client = Trade(my_api_key, my_api_secret, my_api_passphrase, is_sandbox=False)

for my_coin in my_array:
   my_ucoin = my_coin.upper()
   my_coin_funds = my_doc['coins'][my_coin]['funds']
   my_coin_percent = my_doc['coins'][my_coin]['percent']
   print(my_ucoin + ' Start funds: ' + str(my_coin_funds) + ' USDT - Percentage aim:' + str(my_coin_percent) + '%')
   my_log.write(format(datetime.datetime.now()) + ' ' + my_ucoin + ' Start funds: ' + str(my_coin_funds) + ' USDT - Percentage aim: ' + str(my_coin_percent) + '%\n')

   my_orderid = 0
   try:
     my_orderid = my_doc['coins'][my_coin]['orderid']
     print(my_orderid)
     my_log.write(format(datetime.datetime.now()) + ' ' + my_orderid + '\n')
   except Exception as e:
     print('No order ID found')
     my_log.write(format(datetime.datetime.now()) + ' No order ID found \n')

   try:
      coin_old = m_client.get_ticker(my_ucoin + '-USDT')
      print('The price of ' + my_ucoin + ' at {} is:'.format(pd.Timestamp.now()), coin_old['price'])
      my_log.write(format(datetime.datetime.now()) + ' The price of ' + my_ucoin + ' at ' + coin_old['price'] + '\n')
      my_doc['coins'][my_coin]['value'] = coin_old

      if my_orderid == 0:
        print('Order now')
        my_log.write(format(datetime.datetime.now()) + ' Order now \n')

        try:
          # Get first buy
          order_id = client.create_market_order(my_ucoin + '-USDT', 'buy', funds=my_coin_funds).get("orderId")
          sleep(5)
          my_doc['coins'][my_coin]['orderid'] = order_id
          order_list = client.get_fill_list(orderId=order_id,tradeType='TRADE')
          order_size = order_list['items'][0]['size']
          my_doc['coins'][my_coin]['ordersize'] = order_size
          my_order = 1
          my_log.write(format(datetime.datetime.now()) + ' ' + my_ucoin + ' order size ' + order_size + '\n')
        except Exception as e:
          print(f'Error placing order: {e}')
          my_log.write(format(datetime.datetime.now()) + ' Error placing order for ' + my_ucoin + '\n')
        # Save price only after buy for calculating profits
        with open(my_config, 'w') as sfile:
          yaml.dump(my_doc, sfile)

   except Exception as e:
      print(f'Error obtaining ' + my_coin + ' data: {e}')
      my_log.write(format(datetime.datetime.now()) + ' Error obtaining ' + my_ucoin + 'data {e} \n')

my_log.close()

# Loop through Coins and scan profit
while True:
   for my_coin in my_array:

      my_timer = len(my_array)
      sleep(300 / my_timer)

      my_log = open(my_logfile, "a")

      my_ucoin = my_coin.upper()
      my_coin_percent = my_doc['coins'][my_coin]['percent']
      my_price = my_doc['coins'][my_coin]['value']['price']
      my_coin_funds = my_doc['coins'][my_coin]['funds']
      my_orderid = my_doc['coins'][my_coin]['orderid']
      my_ordersize = my_doc['coins'][my_coin]['ordersize']

      try:
        coin_new = m_client.get_ticker(my_ucoin + '-USDT')
        print('The price of ' + my_ucoin + ' at {} is:'.format(pd.Timestamp.now()), coin_new['price'])
        my_log.write(format(datetime.datetime.now()) + ' The price of ' + my_ucoin + ' is:' +coin_new['price'] + '\n')

      except Exception as e:
        print(f'Error obtaining ' + my_ucoin + ' data: {e}')
        my_log.write(format(datetime.datetime.now()) + ' Error obtaining ' + my_ucoin + ' data: {e}')

      percent = round((((float(coin_new['bestAsk']) - float(my_price)) * 100) / float(my_price)),2)
      print('A ' + str(percent) + '% change between the Bought price: ' + str(my_price) + ' and the current price ' + str(coin_new['bestAsk']))
      my_log.write(format(datetime.datetime.now()) + ' A ' + str(percent) + '% change between the Bought price: ' + str(my_price) + ' and the current price ' + str(coin_new['bestAsk']) + '\n')

      if my_orderid == 0:
         if percent < -abs(my_coin_percent):
            # Buy when price is percentage lower than original
            coin_old = m_client.get_ticker(my_ucoin + '-USDT')
            order_id = client.create_market_order(my_ucoin + '-USDT', 'buy', funds=my_coin_funds).get("orderId")
            sleep(5)
            order_list = client.get_fill_list(orderId=order_id,tradeType='TRADE')
            order_size = order_list['items'][0]['size']
            my_doc['coins'][my_coin]['orderid'] = order_id
            my_doc['coins'][my_coin]['ordersize'] = order_size

            my_log.write(format(datetime.datetime.now()) + ' Buy ' + order_size + ' amount of ' + my_ucoin + '\n')
            with open(my_config, 'w') as sfile:
               yaml.dump(my_doc, sfile)

      else:
         if percent >= my_coin_percent:
            # Sell if price is percentage higher than original
            coin_old = m_client.get_ticker(my_ucoin + '-USDT')
            order = client.create_market_order(my_ucoin + '-USDT', 'sell', size=my_ordersize)
            my_doc['coins'][my_coin]['orderid'] = 0
            my_doc['coins'][my_coin]['ordersize'] = 0

            my_log.write(format(datetime.datetime.now()) + ' Sell ' + my_ordersize + ' of ' + my_ucoin + ' with a profit of more than ' + percent + '%\n')
            with open(my_config, 'w') as sfile:
               yaml.dump(my_doc, sfile)

      my_log.close()
