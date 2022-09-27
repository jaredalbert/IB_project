'''most of the code was found here. full credit to the author: Jignesh Davda,

Interactive Brokers Python API (Native) - A Step-by-step Guide - AlgoTrading101 Blog'''

 

from ibapi.client import EClient

from ibapi.wrapper import EWrapper

from ibapi.contract import Contract

 

import threading

import datetime

import time

 

class IBapi(EWrapper, EClient):

                def __init__(self):

                                EClient.__init__(self, self)

                                self.data = [] #Initialize variable to store candle

 

                def historicalData(self, reqId, bar):

                                self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])

                               

def run_loop():

                app.run()

 

app = IBapi()

app.connect('127.0.0.1', 7496, 123)

 

#Start the socket in a thread

api_thread = threading.Thread(target=run_loop, daemon=True)

api_thread.start()

 

time.sleep(1) #Sleep interval to allow time for connection to server

 

#Create contract object

stock = Contract()

stock.symbol = 'SPY'

stock.secType = 'STK'

stock.exchange = 'SMART'

stock.currency = "USD"

 

queryTime = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y%m%d %H:%M:%S")

 

 

#Request historical candles

 

app.reqHistoricalData(4102, stock, queryTime,"100 D", "10 mins", "MIDPOINT", 1, 1, False, [])

time.sleep(5) #sleep to allow enough time for data to be returned

 

#Working with Pandas DataFrames

import pandas

 

df = pandas.DataFrame(app.data, columns=['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume'])

#df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s')

df.to_csv('stock.csv') 

 

print(df)

 