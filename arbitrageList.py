from decimal import Decimal, ROUND_HALF_UP
class ArbitrageList:
    def __init__(self):
        self.scores = {}
        self.sorted_keys = []

    def add_score(self, key, score):
        self.scores[key] = Decimal(score).quantize(Decimal('1e-6'), rounding=ROUND_HALF_UP)
        self._update_sorted_keys()

    def _update_sorted_keys(self):
        self.sorted_keys = sorted(self.scores, key=lambda x: abs(self.scores[x]), reverse=True)

    def display_arbitrageList(self):
        if self.sorted_keys : print("ArbitrageList:")
        for i, key in enumerate(self.sorted_keys, start=1):
            print(f"{i}. {key}: {self.scores[key]}")