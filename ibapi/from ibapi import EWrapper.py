 from ibapi import EWrapper
 from ibapi import EClient


 class IBapi(EWrapper, EClient):
                def __init__(self):
                    EClient.__init__(self, self)

                def nextValidId(self, orderId: int):
                    super().nextValidId(orderId)
                    self.nextorderId = orderId
                    print('The next valid order id is: ', self.nextorderId)

                def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
                    print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
    
                def openOrder(self, orderId, contract, order, orderState):
                    print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

                def execDetails(self, reqId, contract, execution):
                    print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)


            def run_loop():
                app.run()

            app = IBapi()
            app.connect('127.0.0.1', 7497, 0)
            app.nextorderId = None

                #Start the socket in a thread
            api_thread = threading.Thread(target=run_loop, daemon=True)
            api_thread.start()

                #Check if the API is connected via orderid
            while True:
                if isinstance(app.nextorderId, int):
                    print('connected')
                    break
                else:
                    print('waiting for connection')  