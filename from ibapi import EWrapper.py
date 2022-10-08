from ibapi.wrapper import EWrapper
from ibapi.client import EClient
import threading
import datetime
import time



class IBAPI(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        
        
def run_loop():
    IB.run()

IB = IBAPI()
IB.connect('127.0.0.1', 7497, 123)



api_thread = threading.Thread(target=run_loop) 
api_thread.start()



