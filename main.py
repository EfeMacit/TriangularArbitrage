from connector import SocketClient
from dataset import Opportunity
from engine import Engine
import config

baseUrl= f"wss://stream.binance.com:9443/ws/"
def main():

    myengine = Engine() #initilizing engine for arbitrage operations
    myOpportunity = Opportunity(myengine,config.orderbooks) #initiliazing opportunity for datafeed to engine
    mysocketclient = SocketClient(baseUrl, myOpportunity,config.orderbooks) #getting broadcast data
    mysocketclient.start()


if __name__ == "__main__":
   main()
