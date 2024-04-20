# kucoin-bot
### This Kucoin bot is a very simple script written in Python.

The yaml config contains the API details and the coins you like to trade, you can add any coin that Kucoin supports.
In the config 2 values are needed per coin. 
- funds: This is the amount of USDT you like to trade with for this coin
- percent: This is the percentage of profit you aim for.

## How the bot works
It starts with the initial buy of all of the given coins with the given funds. 
Then it starts looping through the coins and checks every 5 minutes for a change in the price on the market. If the change reaches a limit of the given percnetage of the coin it will sell the coin agains the profit. 
When the coin is sold the bot will see if the price drops again with the given percentage under the price af the sale, if it reaches that price it will buy the coin again using the given funds.

## Be carefull!
### Usage of this script is at your own risk, you could lose you investment!
If the price drops the bot holds on to the coin, if you do not want to HODL you need to sell manually. 

## How to setup
Clone this repo in /opt/ and configure your wanted coins and setup you API key info in the kucoin-bot.yml file.

