# kucoin-bot
### This Kucoin bot is a very simple script written in Python.

The yaml config contains the API details and the coins you like to trade, you can add any coin that Kucoin supports.  
In the config 2 values are needed per coin.   
- funds: This is the amount of USDT you like to trade with for this coin.  
- percent: This is the percentage of profit you aim for.  

## How the bot works
It starts with the initial buy of all of the given coins with the given funds.   
Then it starts looping through the coins and checks every 5 minutes for a change in the price on the market. If the change reaches a limit of the given percentage of the coin the bot will sell the coin and collect the profit.   
When the coin is sold the bot will look if the price drops again with the given percentage under the price of the sale. If it reaches that lower price it will buy the coin again using the given funds.  

## Be carefull!
### Usage of this script is at your own risk, you could lose you investment!
If the price drops the bot holds on to the coin, if you do not want to HODL you need to sell manually.  
- Maybe in the future I will create a limit for sale when dropping below certain point.

## Telegram notifications
If you enable Telegram support in the config and add the token for your Telegram bot, you can receive messages when coins are sold or bought.   
- Maybe in the future I will add remote management of your sales/buys from Telegram.

## How to setup
Clone this repo in /opt/ and configure your wanted coins and setup you API key info in the kucoin-bot.yml file.

The script itself has no output, you can run it as a service. To create the service follow these steps:

Create a file : /etc/systemd/system/kucoin-bot.service

```
[Unit]
Description=Kucoin-bot
After=multi-user.target
[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /opt/kucoin-bot/kucoin-bot.py
[Install]
WantedBy=multi-user.target
```
 Then run :  
 sudo systemctl daemon-reload  
 sudo systemctl enable kucoin-bot.service  
   
 And after you updated your kucoin-bot.yml file run:  
 sudo systemctl start kucoin-bot.service  
  
 If you would run:  
 sudo systemctl status kucoin-bot.service  
  
 You should see no errors.  
 You could also check /var/log/kucoin.log   
  
## Disclamer
 This bot is just a hobby project!  
 Using this is at your own risk as it is mine when I use this.   
 If you notice any issues please let me know.   