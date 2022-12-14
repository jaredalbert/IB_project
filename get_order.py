from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import * 
from ibapi.order import * 

import threading
import pickle
import datetime 
import time 
import math
import queue





def contractCreate():
    # Fills out the contract object
    contract1 = Contract()  # Creates a contract object from the import
    contract1.symbol = "VIEW"   # Sets the ticker symbol 
    contract1.secType = "STK"   # Defines the security type as stock
    contract1.currency = "USD"  # Currency is US dollars 
    # In the API side, NASDAQ is always defined as ISLAND in the exchange field
    contract1.exchange = "SMART"
    #contract1.PrimaryExch = "ISLAND"
    return contract1    # Returns the contract object

def orderCreate():
    # Fills out the order object 
    order1 = Order()    # Creates an order object from the import
    order1.action = "BUY"   # Sets the order action to buy
    order1.orderType = "MKT"    # Sets order type to market buy
    order1.transmit = True
    #order1.lmtPrice = .22
    order1.totalQuantity = 15   # Setting a static quantity of 10 
    return order1   # Returns the order object 

def orderExecution(app, order_id):
    
    #Places the order with the returned contract and order objects 
    contractObject = contractCreate()
    orderObject = orderCreate()
    nextID = order_id
    app.placeOrder(nextID, contractObject, orderObject)
    print(f"order was placed with nextID: {nextID, contractObject, orderObject}")
    

class TestWrapper(EWrapper):

    
    
    #error handling methods

    def init_error(self):
        error_queue =  queue.Queue()
        self.my_errors_queue = error_queue
    
    def is_error(self):
        error_exist = not self.my_errors_queue.empty()
        return error_exist
    
    def get_error(self, timeout=6):
        if self.is_error():
            try:
                 return self.my_errors_queue.get(timeout=timeout)
            except queue.Empty:
                return None
        return None

    def error(self, id,errorCode, errorString):
        errormessage = f"IB returns an error with {id} errorcode {errorCode} that says {errorString})"
        self.my_errors_queue.put(errormessage)

    #time methods

    def init_time(self):
        time_queue = queue.Queue()
        self.my_time_queue = time_queue
        return time_queue 

    def currentTime(self, server_time):
        ##overridden method in EWrapper Class
        self.my_time_queue.put(server_time)


class TestClient(EClient):
    
    def __init__ (self, wrapper):
        EClient.__init__(self, wrapper)

    def server_clock(self):

        print ('Asking the server for Unix time')

        #creats a queue tp store the time
        time_storage = self.wrapper.init_time()

        #sets up a request for unix time from the Eclint

        self.reqCurrentTime()

        max_wait_time = 10

        try:
            requested_time = time_storage.get(timeout= max_wait_time)

        except queue.Empty:
            print ('the queue is empty or max time reached')
            requested_time = None

        while self.wrapper.is_error():
            print ('Error:')
            print (self.get_error(timeout=5))

        return requested_time

class TestApp(TestWrapper, TestClient):
    #initializes our main classes
    def __init__(self, ipadressm, portid, clientid):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)

        #connects to the server with the ipaddress, portid, and clientid specified in the program
        self.connect(ipadressm, portid, clientid)

        #initializes the threading 
        thread = threading.Thread(target = self.run)
        thread.start()
        setattr(self, "_thread", thread)

        #start listening for errors
        self.init_error()



def place_order():    
    
    print ('before start')
    
    app = TestApp('127.0.0.1', 7497, 0)
    time.sleep(2)
    print ('The program has begun')

    requested_time = app.server_clock()

    
    print("")
    print ('This is the current time from the server ')
    print (requested_time)

    
    
    with open ('pickle.pk','rb') as file:#this persists the orderID since 
        order_id = pickle.load(file) #the API needs a new unique number for each order
        

    
    orderExecution(app, order_id) 

    order_id += 1

    with open('pickle.pk', 'wb') as file:
        pickle.dump(order_id, file)
    
    
    print('order id: ', order_id)
    app.disconnect()


if __name__ == '__main__':
    
    for _ in range(2):
        place_order()
        print('placed')
    

   
   
    

'''   
if "__main__" == __name__:
    print ('before start')
    
    app = TestApp('127.0.0.1', 7497, 0)
    
    print ('The program has begun')

    requested_time = app.server_clock()

    
    print("")
    print ('This is the current time from the server ')
    print (requested_time)

    #app.disconnect()


time.sleep(2)
orderExecution(app)
print (order_id)


'''
def add():
    return 3 + 4

def submit_function():
    x = add()
    print (f'{x} submit function was pressed')