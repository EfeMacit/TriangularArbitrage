import bisect
from arbitrageList import ArbitrageList
from config import orderbookpairs


class Engine:
    """"Applying arbitrage operations and updates arbitragelist"""

    def __init__(self):
        self.orderbooks = orderbookpairs
        self.arbitragelist = ArbitrageList()
        self.combinations = self.getCombinations()

    def do_arbitrage(self, opportunities):
        """Applying arbitrage operations"""
        for i in self.combinations:
            A = opportunities[i['base']]
            B = opportunities[i['mid']]
            C = opportunities[i['last']]
            if all(value != 0 for value in
                   (A['ask_price'], B['ask_price'], C['ask_price'], A['bid_price'], B['bid_price'], C['bid_price'])):
                arb_calc1 = A['ask_price'] * B['ask_price'] * 1 / C['bid_price']
                arb_calc2 = A['bid_price'] * B['bid_price'] * 1 / C['ask_price']
                # commission rate %0.1 generally arbitrage rate %0.0001
                if (arb_calc1 < 1):
                    self.arbitragelist.add_score(i['base'] + i['mid'] + i['last'], arb_calc1 - 1)
                    print(i['base'], " buy order", A['ask_price'], "  ", i['mid'], " buy order ", B['ask_price'], "  ",
                          i['last'], "  sell order ", C['bid_price'])
                elif (arb_calc2 > 1):
                    self.arbitragelist.add_score(i['base'] + i['mid'] + i['last'], arb_calc1 - 1)
                    print(i['base'], " sell order", A['ask_price'], "  ", i['mid'], " sell order ", B['ask_price'],
                          "  ", i['last'], "  buy order ", C['bid_price'])
                self.arbitragelist.display_arbitrageList()

    def getCombinations(self):
        """Returns possible combinations for applying arbitrage operations"""
        """These operations can be handled with numpy also"""
        combinations = []
        for symbol1 in self.orderbooks:
            symbol1_pair1 = symbol1.split('/')[0]
            symbol1_pair2 = symbol1.split('/')[1]
            for symbol2 in self.orderbooks:
                symbol2_pair1 = symbol2.split('/')[0]
                symbol2_pair2 = symbol2.split('/')[1]
                if (symbol1_pair2 == symbol2_pair1):
                    for symbol3 in self.orderbooks:
                        symbol3_pair1 = symbol3.split('/')[0]
                        symbol3_pair2 = symbol3.split('/')[1]
                        if ((symbol2_pair2 == symbol3_pair2) and (symbol3_pair1 == symbol1_pair1)):
                            combination = {'base': (symbol1_pair1 + symbol1_pair2).upper(),
                                           'mid': (symbol2_pair1 + symbol2_pair2).upper(),
                                           'last': (symbol3_pair1 + symbol3_pair2).upper()}
                            combinations.append(combination)
        return combinations
