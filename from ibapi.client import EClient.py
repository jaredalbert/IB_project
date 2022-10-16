from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange,
              ':', order.action, order.orderType, order.totalQuantity, orderState.status)

        self.reqAllOpenOrders()

def run_loop():
    app.run()

app = IBapi()
app.connect('127.0.0.1', 7497, 0)
print('connected')
app.reqAllOpenOrders()
# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(3)
app.disconnect()