#
import datetime as dt


class Wallet:
    def __init__(self):
        self.__investments = {}

    @property
    def investments(self):
        return list(self.__investments.values())

    @property
    def value_inv(self):
        return sum(invest.value_inv for invest in self.investments)

    @property
    def value(self):
        return sum(invest.value for invest in self.investments)

    @property
    def income(self):
        return self.value / self.value_inv - 1

    def invest(self, tag, category, value=None, amount=1, price=0, date=dt.date.today()):
        if value:
            self.__investments.update({tag: category(1, value, date)})
        else:
            self.__investments.update({tag: category(amount, price, date)})
