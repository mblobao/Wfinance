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
        return sum(app[0] * app[1] * ((1 + self.__inc) ** ((td - app[2]).days / 365) - 1) for app in self.__applications)

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
    
    def __init__(self, income, tax=0, fee=0, income_period='year'):
        super().__init__(income, tax, fee, income_period)



class RV(Invest):
    def __init__(self):
        pass
# TODO: Formular classe de renda variável