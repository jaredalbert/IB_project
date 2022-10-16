from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import * 
from threading import Timer

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqid, errorCode, errorString):
       print ('Error: ', reqid, " ",errorCode," ", errorString)

    def nextValidID(self, orderId): 
        self.nextOrderId = orderId
        self.start()

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld,mktCapPrice):
        print("OrderStatus Id :", orderId, " ", status, " ", filled, remaining, avgFillPrice, permId, lastFillPrice, clientId, whyHeld, mktCapPrice)
    
    def openOrder(self, orderId, contract, order, orderState):
        print("openOrder id: ", orderId, contract, order, orderState)
    
    def execDetails(self, reqId, contract, execution):
        print('ExecDetails: ', reqid, contract.symbol, contract.secType, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)
    
        self.reqAllOpenOrders()
       

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
        order.lmtPrice = 15

        self.placeOrder(self.nextOrderId, contract, order)
        

    def stop(self):
        self.done = True
        self.disconnect()

def main():
    app = TestApp()
    app.nextValidID(0)
    app.connect('127.0.0.1', 7497, 0)

   
    #app.reqAllOpenOrders()
    Timer(3, app.stop).start()
    app.start()
    app.reqAllOpenOrders()
    app.run()
    
    

if __name__ == '__main__':
    main()




        



    
