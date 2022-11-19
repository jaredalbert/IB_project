from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import * 
from threading import Timer
import pickle
from time import sleep

l = []

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqid, errorCode, errorString):
       print ('Error: ', reqid, " ",errorCode," ", errorString)

    def nextValidID(self, orderId): 
        self.nextOrderId = orderId
        self.start()

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld,mktCapPrice):
        #keys=(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld,mktCapPrice)
        #items =("OrderStatus Id :", orderId, " ", status, " ", filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        #print (dict(zip(keys, items)))
        pass
    
    def openOrder(self, orderId, contract, order, orderState):
        global l
        keys = ('orderId', 'contract', 'order', 'orderState')
        items = ( orderId, contract, order, orderState)
        dict_of_order_details = (dict(zip(keys, items)))
        l.append(dict_of_order_details)
        with open('pickle2.pk','wb') as f:
            pickle.dump(l, f)
        #print(f'order details: {l}')
        #print("")
        #print ('list of dictionaries: ', l)
        return l

    def execDetails(self, reqId, contract, execution):
        #print('ExecDetails: ', reqid, contract.symbol, contract.secType, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)
    
        self.reqAllOpenOrders()
        #return dict_of_order_details

    def start(self):
        contract = Contract()
        contract.symbol = 'AAPL'
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        #contract.primaryExchange = 'NASDAQ'
        

        order = Order()
        order.action = 'BUY'
        order.totalQuantity = 10
        order.transmit = True
        order.orderType = 'LMT'
        order.lmtPrice = 15.10

        self.placeOrder(self.nextOrderId, contract, order)
        
    

        


        


    def stop(self):
        self.done = True
        self.disconnect()

def get_orders():
    global l
    app = TestApp()
    app.nextValidID(8029)
    app.connect('127.0.0.1', 7497, 0)

   
    #app.reqAllOpenOrders()
    Timer(3, app.stop).start()
    app.start()
    app.reqAllOpenOrders()
    app.reqAutoOpenOrders(True)
    app.reqOpenOrders()
    #sleep(3)
    #app.cancelOrder(8027)
    #print (l)
    

    app.run()
    
    with open('pickle2.pk', 'rb') as f:
        orders = pickle.load(f)
    print (orders)
    

if __name__ == '__main__':
   get_orders()




        



    
