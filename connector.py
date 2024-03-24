import json
import websocket  # client
from threading import Thread
from dataset import Opportunity


class SocketClient:
    """"Retrieving bookticker data from binance websocket"""

    def __init__(self, baseurl: str, opportunity: Opportunity, orderbooks: list):
        self.baseurl = baseurl
        self.opportunity = opportunity
        self.connections = []
        self.connection_orderbooks = orderbooks
        self.arbitrage_opportunities = {}

    def on_message(self, ws, message):  # can be ascynchron but this is more readable than thread call back
        response = json.loads(message)
        currency = response['s']
        bid_price = float(response['b'])
        ask_price = float(response['a'])
        self.opportunity.change_opportunity(currency, {'bid_price': bid_price, 'ask_price': ask_price})

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def generateUrls(self):
        for i in self.connection_orderbooks:
            connection = f"{self.baseurl}{i}@bookTicker"
            self.connections.append(connection)

    def start_listener(self, url):
        ws = websocket.WebSocketApp(url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.run_forever()

    def start(self):
        self.generateUrls()
        for url in self.connections:  # for every connection there should be a seperate thread in order to get all data in parallel
            thread = Thread(target=self.start_listener, args=(url,))
            thread.start()
