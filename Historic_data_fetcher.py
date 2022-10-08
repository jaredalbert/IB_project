# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 09:04:26 2020

@author: Windows10
"""
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData

import datetime

class MyWrapper(EWrapper):

    def nextValidId(self, orderId:int):
        #4 first message received is this one
        print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        #5 start requests here
        self.start()

    def historicalData(self, reqId:int, bar: BarData):
        #7 data is received for every bar
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        #8 data is finished
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
        #9 this is the logical end of your program
        app.disconnect()
        print("finished")

    def error(self, reqId, errorCode, errorString):
        # these messages can come anytime.
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

    def start(self):
        queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")

        fx = Contract()
        fx.secType = "STK" 
        fx.symbol = "REFR"
        #fx.currency = "JPY"
        fx.exchange = "SMART"

        #6 request data, using fx since I don't have Japanese data
        app.reqHistoricalData(4102, fx, queryTime,"1 M", "1 day", "MIDPOINT", 1, 1, False, [])

app = EClient(MyWrapper()) #1 create wrapper subclass and pass it to EClient
app.connect("127.0.0.1", 7497, clientId=123) #2 connect to TWS/IBG
app.run() #3 start message thread


