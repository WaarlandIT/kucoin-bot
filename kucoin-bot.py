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

my_config = '/opt/kucoin-bot/kucoin-bot.yml'
my_logfile = '/var/log/kucoin-bot.log'

with open(my_config, 'r') as file:
    my_doc = yaml.safe_load(file)

    if not 'stats' in my_doc.items():
        my_doc['stats'] = dict(percentage_today=0)

my_api_key = my_doc['api']['key']
my_api_passphrase = my_doc['api']['pass']
my_api_secret = my_doc['api']['secret']

my_array = my_doc['coins']
m_client = Market(url='https://api.kucoin.com')
client = Trade(my_api_key, my_api_secret, my_api_passphrase, is_sandbox=False)
my_log = open(my_logfile, "a")

def buy_coins():
  try:
    coin_old = m_client.get_ticker(my_ucoin + '-USDT')
    my_log.write(format(datetime.datetime.now()) + ' Buy coins now \n')
    order_id = client.create_market_order(my_ucoin + '-USDT', 'buy', funds=my_coin_funds).get("orderId")
    sleep(5)
    my_doc['coins'][my_coin]['orderid'] = order_id
    order_list = client.get_fill_list(orderId=order_id,tradeType='TRADE')
    order_size = order_list['items'][0]['size']
    my_doc['coins'][my_coin]['ordersize'] = order_size
    my_order = 1
    my_log.write(format(datetime.datetime.now()) + ' Bought ' + order_size + ' amount of ' + my_ucoin + '\n')
    my_telegram_message = format(datetime.datetime.now()) + ' Bought ' + order_size + ' amount of ' + my_ucoin
  except Exception as e:
    my_log.write('------------------')
    my_log.write(format(datetime.datetime.now()) + ' Error placing order for ' + my_ucoin + '\n')
    my_log.write('------------------')
    my_telegram_message = format(datetime.datetime.now()) + ' Error placing order for ' + my_ucoin
    pass

  # Save price only after buy for calculating profits
  with open(my_config, 'w') as sfile:
    yaml.dump(my_doc, sfile)

  send_telegram(my_telegram_message)
# End function buy_coins

def sell_coins():
  try:
    coin_old = m_client.get_ticker(my_ucoin + '-USDT')
    my_log.write(format(datetime.datetime.now()) + ' Sell ' + my_ordersize + ' of ' + my_ucoin + ' with a profit of more than ' + str(percent) + '%\n')
    order = client.create_market_order(my_ucoin + '-USDT', 'sell', size=my_ordersize)
    my_doc['coins'][my_coin]['orderid'] = 0
    my_doc['coins'][my_coin]['ordersize'] = 0
    my_log.write(format(datetime.datetime.now()) + ' Sale complete\n')
    my_telegram_message = format(datetime.datetime.now()) + ' Sell ' + my_ordersize + ' of ' + my_ucoin + ' with a profit of more than ' + str(percent)
  except Exception as e:
    my_log.write('------------------')
    my_log.write(format(datetime.datetime.now()) + ' Error selling ' + my_ucoin + ' data: {e}')
    my_log.write('------------------')
    my_telegram_message = format(datetime.datetime.now()) + ' Error selling ' + my_ucoin + ' data: {e}'
    pass

  with open(my_config, 'w') as sfile:
      yaml.dump(my_doc, sfile)
  send_telegram(my_telegram_message)
# End function sell_coins

def initialize_coins():
  my_log.write('########### \n' + format(datetime.datetime.now()) + ' Start bot \n')
  for my_coin in my_array:
    my_ucoin = my_coin.upper()
    my_coin_funds = my_doc['coins'][my_coin]['funds']
    my_coin_percent = my_doc['coins'][my_coin]['percent']
    my_log.write(format(datetime.datetime.now()) + ' ' + my_ucoin + ' Start funds: ' + str(my_coin_funds) + ' USDT - Percentage aim: ' + str(my_coin_percent) + '%\n')

    my_orderid = 0
    try:
      my_orderid = my_doc['coins'][my_coin]['orderid']
      my_log.write(format(datetime.datetime.now()) + ' ' + my_orderid + '\n')
    except Exception as e:
      my_log.write(format(datetime.datetime.now()) + ' No order ID found \n')

    try:
        coin_old = m_client.get_ticker(my_ucoin + '-USDT')
        my_log.write(format(datetime.datetime.now()) + ' The price of ' + my_ucoin + ' at ' + coin_old['price'] + '\n')
        my_doc['coins'][my_coin]['value'] = coin_old

        if my_orderid == 0:
          my_log.write(format(datetime.datetime.now()) + ' Order now \n')
          buy_coins()

    except Exception as e:
        my_log.write('------------------')
        my_log.write(format(datetime.datetime.now()) + ' Error obtaining ' + my_ucoin + 'data {e} \n')
        my_log.write('------------------')
        pass

  my_telegram_message = format(datetime.datetime.now()) + ' Bot started'
  send_telegram(my_telegram_message)

  my_log.close()
# End function initialize_coins

def send_telegram(my_telegram_message):
  if str(my_doc['telegram']['token']) != 'no':
    my_token = my_doc['telegram']['token']
    url = f"https://api.telegram.org/bot{my_token}/getUpdates"
    my_result = requests.get(url).json()
    my_chatid = my_result['result'][0]['message']['chat']['id']
    url = f"https://api.telegram.org/bot{my_token}/sendMessage?chat_id={my_chatid}&text={my_telegram_message}"
    my_log.write(str(requests.get(url).json()))
    
# End function send_telegram

initialize_coins()

# Loop through Coins and scan profit
while True:
   for my_coin in my_array:

      sleep(300 / len(my_array))

      my_log = open(my_logfile, "a")

      my_ucoin = my_coin.upper()
      my_coin_percent = my_doc['coins'][my_coin]['percent']
      my_price = my_doc['coins'][my_coin]['value']['price']
      my_coin_funds = my_doc['coins'][my_coin]['funds']
      my_orderid = my_doc['coins'][my_coin]['orderid']
      my_ordersize = my_doc['coins'][my_coin]['ordersize']

      try:
        coin_new = m_client.get_ticker(my_ucoin + '-USDT')
        my_log.write(format(datetime.datetime.now()) + ' The price of ' + my_ucoin + ' is:' +coin_new['price'] + '\n')

      except Exception as e:
        my_log.write('------------------')
        my_log.write(format(datetime.datetime.now()) + ' Error obtaining ' + my_ucoin + ' data: {e}')
        my_log.write('------------------')
        pass

      # Percentage calc
      percent = round((((float(coin_new['bestAsk']) - float(my_price)) * 100) / float(my_price)),2)

      my_log.write(format(datetime.datetime.now()) + ' A ' + str(percent) + '% change between the Bought price: ' + str(my_price) + ' and the current price ' + str(coin_new['bestAsk']) + '\n')
      my_doc['stats']['percentage_today'] = ((my_doc['stats']['percentage_today'] + percent) / 2)
      my_doc['coins'][my_coin]['value']['percent'] = percent

      with open(my_config, 'w') as sfile:
          yaml.dump(my_doc, sfile)

      if my_orderid == 0:
         if percent < -abs(my_coin_percent):
            # Buy when price is percentage lower than original
            buy_coins()
      else:
         if percent >= my_coin_percent:
            # Sell if price is percentage higher than original
            sell_coins()

      my_log.close()
