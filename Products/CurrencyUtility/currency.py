import math

from zope.interface import implements
from zope.component import getUtility
from Products.CurrencyUtility.interfaces import ICurrencyUtility, ICurrencyAware

class CurrencyAware(object):
    """helper class to convert values between currencies"""
    implements(ICurrencyAware)

    value = 0

    def __str__(self):
        return self.toString()

    def __init__(self, value, currency=None, rounding=None):
        """value is a price and IT's currency"""
        self.utility = getUtility(ICurrencyUtility)
        if currency is not None:
            value = float(value)/self.utility.getCurrencyFactor(currency)
        self.value = value
        if rounding is not None:
            self.rounding = rounding
        else:
            rounding = 0.05 # default value, round to 5 cents

    def getCurrencySymbol(self):
        """returns the currency symbol"""
        return self.utility.getActiveCurrency()

    def getValue(self, currency=None):
        """returns the value in the appropriate currency"""
        factor = self.utility.getCurrencyFactor(currency)
        return float(self.value) * factor

    def getRoundedValue(self, currency=None):
        """returns the value in the appropriate currency rounded to 0.05"""
        value = self.getValue(currency)
        factor = 1.0 / self.rounding
        return float(int(math.ceil(value*factor)))/factor

    def toString(self, currency=None):
        """returns the value in the appropriate currency rounded to 0.05 including the symbol"""
        return "%s %0.2f" % (self.utility.getCurrencySymbol(currency), self.getRoundedValue(currency))

    def valueToString(self, currency=None):
        """returns the value in the appropriate currency rounded to 0.05"""
        return "%0.2f" % self.getRoundedValue(currency)

    def safeToString(self, currency=None):
        """returns the value in the appropriate currency rounded to 0.05 including the currency-short-name"""
        return "%s %0.2f" % (self.utility.getActiveCurrency(currency), self.getRoundedValue(currency))
