import asyncio
import json
import datetime
from websocket import create_connection
"""This is unnecessary only for different socket implementations"""
class connector:
    def __init__(self, baseurl):
        self.baseurl = baseurl
        self.connections = []
        self.connection_orderbooks = ["btcusdt", "btctry", "btceur", "ethbtc", "ethusdt", "etheur"]
        self.currencies_to_check = set()
        self.arbitrage_opportunities = {}

    def generateUrls(self):
        for i in self.connection_orderbooks:
            connection = f"{self.baseurl}{i}@bookTicker"
            self.connections.append(connection)
            base_currency = i.upper()
            self.currencies_to_check.add(base_currency)
        print("generate url")

    async def getData(self):
        arbs = []

        # for url in self.connections:
        #     await self.iterate(url, self.arbitrage_opportunities, self.currencies_to_check)
        #     # arbs.append(myx)

        # tasks = [self.iterate(url, self.arbitrage_opportunities, self.currencies_to_check) for url in self.connections]
        # arbs = await asyncio.gather(*tasks, return_exceptions=True)
        print("data begin:", datetime.datetime.now() )
        # await self.iterate(self.connections[0], self.arbitrage_opportunities, self.currencies_to_check)

        tasks = [self.iterate(url) for url in self.connections]
        await asyncio.gather(*tasks, return_exceptions=True)
        print("data end:", datetime.datetime.now() )
        # return self.arbitrage_opportunities

    async def other_iteration(self, url):
        print("socket:", datetime.datetime.now() )
        async with asyncio.CustomContextManager() as manager:
            ws=create_connection(url)  # open socket
            response = ws.recv()  # receive from socket
            # print("socket:", datetime.datetime.now() )
            # print (response)
            ws.close()  # close socket
        return response
    
    def get_data_other(self):
        arbs = []

        for url in self.connections:
            ws = create_connection(url)  # open socket
            response = ws.recv()  # receive from socket
            print("socket:", datetime.datetime.now() )
            # print (response)
            arbs.append(response)
            # ws.close()  # close socket
        return arbs

    async def iterate(self, url):
        print("iterate worked", datetime.datetime.now())
        async with websockets.connect(url) as ws:
            while (True):
                response = await asyncio.wait_for(ws.recv(), timeout=None)
                response = json.loads(response)
                currency = response['s']
                bid_price = float(response['b'])
                ask_price = float(response['a'])
                print(currency,  {'bid_price': bid_price, 'ask_price': ask_price} , datetime.datetime.now())

            # self.arbitrage_opportunities[currency] = {'bid_price': bid_price, 'ask_price': ask_price}
            # print("socket worked:" , datetime.datetime.now())
            # await ws.close()
            
        # print("socket end:", datetime.datetime.now() )
    
