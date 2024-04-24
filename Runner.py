#!/usr/bin/python3
import sys
import pandas as pd

from kucoin.client import Market

m_client = Market(url='https://api.kucoin.com')

my_coin = 'BTC'

my_data = m_client.get_ticker(my_coin + '-USDT')

print(my_data)
