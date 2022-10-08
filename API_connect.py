



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

app.connect('127.0.0.1', 7497, 123)



#Start the socket in a thread

api_thread = threading.Thread(target=run_loop, daemon=True)

api_thread.start()



time.sleep(1) #Sleep interval to allow time for connection to server

""" if __name__ == '__main__':
    api_connect() """