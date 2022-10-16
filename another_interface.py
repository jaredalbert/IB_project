from sys import argv
from time import sleep, strftime

from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.execution import Execution


def showmessage(message, mapping):
    try:
        del(mapping['self'])
    except (KeyError, ):
        pass
    items = mapping.items()
    #items.sort()
    print ('### {message}')
    for k, v in items:
        print (f'   {k} , {v}')


class ReferenceWrapper(EWrapper):
    def __init__ (self,subs={}):
        super(ReferenceWrapper, self).__init__()
        self.orderID = None
        self.subscriptions = subs

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeId):
        showmessage('orderStatus', vars())

    def openOrder(self, orderId, contract, order, state):
        showmessage('openOrder', vars())

    def connectionClosed(self):
        showmessage('connectionClosed', {})

    def execDetails(self, orderId, contract, execution):
        showmessage('execDetails', vars())

    def error(self, id=None, errorCode=None, errorMsg=None):
        showmessage('error', vars())

    def managedAccounts(self, accountsList):
        showmessage('managedAccounts', vars())

    def apiValidId(self, orderId):
        self.orderID = orderId
        showmessage('apiValidId', vars())

    def updateAccountValue(self, key,  value,  currency,  accountName):
        showmessage('updateAccountValue', vars())

    def updatePortfolio(self, contract,  position,  marketPrice,  marketValue,  averageCost,  unrealizedPNL,  realizedPNL,  accountName):
        showmessage('updatePortfolio', vars())

    def updateAccountTime(self, timestamp):
        showmessage('updatePortfolio', vars())


class BaseApp():
    def __init__(self, host='localhost', port=7496, clientId=0,name=None,**kwargs):
        self.host = host
        self.port = port
        self.clientId = clientId
        self.subscriptions = {}
        if 'wrapper' in kwargs.keys():
            self.wrapper = kwargs['wrapper']
            self.wrapper.setSubscriptions(self.subscriptions)
        else:
            self.wrapper = ReferenceWrapper(self.subscriptions)
        self.connection = EClient(self.wrapper)
        self.conid = 1

    def connect(self, host, port, clientId):
        """This function must be called before any other. There is no
        feedback for a successful connection, but a subsequent attempt to
        connect will return the message \"Already connected.\"

        host:str - The host name or IP address of the machine where TWS is
            running. Leave blank to connect to the local host.
        port:int - Must match the port specified in TWS on the
            Configure>API>Socket Port field.
        clientId:int - A number used to identify this client connection. All
            orders placed/modified from this client will be associated with
            this client identifier.

            Note: Each client MUST connect with a unique clientId."""


        try:
            self.host = host
            self.port = port
            self.clientId = clientId
            print("Connecting to %s:%d w/ id:%d", self.host, self.port, self.clientId)

            self.conn = Connection(self.host, self.port)

            self.conn.connect()
            self.setConnState(EClient.CONNECTING)

            #TODO: support async mode

            v100prefix = "API\0"
            v100version = "v%d..%d" % (MIN_CLIENT_VER, MAX_CLIENT_VER)

            if self.connectionOptions:
                v100version = v100version + " " + self.connectionOptions

            #v100version = "v%d..%d" % (MIN_CLIENT_VER, 101)
            msg = comm.make_msg(v100version)
            ##logger.debug("msg %s", msg)
            msg2 = str.encode(v100prefix, 'ascii') + msg
            ##logger.debug("REQUEST %s", msg2)
            self.conn.sendMsg(msg2)

            self.decoder = decoder.Decoder(self.wrapper, self.serverVersion())
            fields = []

            #sometimes I get news before the server version, thus the loop
            while len(fields) != 2:
                self.decoder.interpret(fields)
                buf = self.conn.recvMsg()
                if not self.conn.isConnected():
                    # recvMsg() triggers disconnect() where there's a socket.error or 0 length buffer
                    # if we don't then drop out of the while loop it infinitely loops
                    ##logger.warning('Disconnected; resetting connection')
                    self.reset()
                    return
                ##logger.debug("ANSWER %s", buf)
                if len(buf) > 0:
                    (size, msg, rest) = comm.read_msg(buf)
                    ##logger.debug("size:%d msg:%s rest:%s|", size, msg, rest)
                    fields = comm.read_fields(msg)
                    #logger.debug("fields %s", fields)
                else:
                    fields = []

            (server_version, conn_time) = fields
            server_version = int(server_version)
            #logger.debug("ANSWER Version:%d time:%s", server_version, conn_time)
            self.connTime = conn_time
            self.serverVersion_ = server_version
            self.decoder.serverVersion = self.serverVersion()

            self.setConnState(EClient.CONNECTED)

            self.reader = reader.EReader(self.conn, self.msg_queue)
            self.reader.start()   # start thread
            #logger.info("sent startApi")
            self.startApi()
            self.wrapper.connectAck()
        except:
            pass
            
            """ m """
    """ def eConnect(self):
        self.connection(self.host, self.port, self.clientId)
        try:
            self.host = host
            self.port = port
            self.clientId = clientId
            ##logger.debug("Connecting to %s:%d w/ id:%d", self.host, self.port, self.clientId)

            self.conn = Connection(self.host, self.port)

            self.conn.connect()
            self.setConnState(EClient.CONNECTING)

        except socket.error:
            if self.wrapper:
                self.wrapper.error(NO_VALID_ID, CONNECT_FAIL.code(), CONNECT_FAIL.msg())
            #logger.info("could not connect")
            self.disconnect() """
    def reqAutoOpenOrders(self):
        self.connection.reqAutoOpenOrders(1)

    def reqAllOpenOrders(self):
        self.connection.reqAllOpenOrders()

    def eDisconnect(self):
        sleep(5)
        self.connection.eDisconnect()

    def reqAccountUpdates(self):
        self.connection.reqAccountUpdates(True,"DU666")



if __name__ == '__main__':
    """ run from command prompt and type 'm' hit enter
        manually place / change orders in TWS
        you should see order statuses and executions
    """
    import msvcrt,sys

    app = BaseApp()
    app.connect('127.0.0.1', 7497, 0)
    sleep(5)
    app.reqAutoOpenOrders()
    app.reqAccountUpdates()

    """ while True:
        action = msvcrt.getch()
        print (action)
        if action=='m':
            app.reqAutoOpenOrders()
            app.reqAccountUpdates()
        elif action=='c': 
            sys.exit(1)
"""