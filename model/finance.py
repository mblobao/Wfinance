# 
from datetime import date, time, datetime, timedelta
import datetime as dt
import matplotlib.pyplot as plt
from numpy import pv, pmt, fv, nper, rate


class Invest:
    """
    The applications are tuples with the following sequence:
        (amount, value, initial date)
    """
    def __init__(self, income, tax=0, fee=0, income_period='year'):
        self.__applications = []
        self.__tax = tax
        self.__fee = fee
        if income_period == 'year':
            self.__inc = income
        elif income_period == 'month':
            self.__inc = (1 + income) ** 12 - 1
        
    @property
    def value_inv(self):
        return sum(app[0] * app[1] for app in self.__applications)

    @property
    def tempo(self):
        return [dt.date.today() - app[2] for app in self.__applications]

    @property
        def value(self):
        td = dt.date.today()
        s = 0
        for app in self.__applications:
            s += app[0] * app[1] * ((1 + self.__inc) ** ((td - app[2]).days / 365) - 1)
        return s

    @property
    def income(self):
        return self.__inc
    
    def aplicar(self, value, amount=1, date=dt.date.today()):
        self.__applications.append((amount, value, date))


class RF(Invest):
    @staticmethod
    def imp(dur):
        if dur <= 180:
            return 0.225
        elif dur <= 360:
            return 0.2
        elif dur <= 720:
            return 0.175
        else:
            return 0.15

    def __init__(self, income, income_period='year'):
        super().__init__(income, income_period)
    
    @property
    def tax(self):
        return [self.imp(app[2].days) for app in self.applications]


class RV(Invest):
    def __init__(self, code, price):
        super().__init__(0)
        self.__code = code
        self.__price = price

    @property
    def code(self):
        return self.__code

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, p):  # TODO: Implementar importação automática do valor da ação
        self.__price = p
    
    @property
    def amount(self):
        return sum(app[0] for app in self.applications)

    @property
    def value(self):
        return self.price * self.amount

    @property
    def income(self):
        return self.value / self.value_inv - 1
