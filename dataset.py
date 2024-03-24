from threading import Lock
from engine import Engine
# Declaring a lock
lock = Lock()

class Opportunity:
    def __init__(self, engine : Engine, orderbooks: list):
        self.opportunities = {}
        self.orderbooks = orderbooks

        initvalue = {"bid_price":0,
                     "ask_price":0}
        for i in self.orderbooks:
            self.opportunities[i.upper()] = initvalue
        self.engine = engine
        self.changed = False

    def change_opportunity (self, currency, newjson):
        """do arbitrage operations if there is a change on the data"""
        lock.acquire()#in case of read and write problem/dirty read(read data changed)
        #lock can be removed it was for stability
        try:
            if (self.opportunities[currency] != newjson ):
                self.opportunities[currency] = newjson
                self.engine.do_arbitrage(self.opportunities)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        lock.release()