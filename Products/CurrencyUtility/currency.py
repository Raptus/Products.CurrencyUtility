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

    def __init__(self, value, currency=None):
        """value is a price and IT's currency"""
        if currency is not None:
            utility = getUtility(ICurrencyUtility)
            value = float(value)/utility.getCurrencyFactor(currency)
        self.value = value

    def getValue(self, currency=None):
        """returns the value in the appropriate currency"""
        utility = getUtility(ICurrencyUtility)
        factor = utility.getCurrencyFactor(currency)
        return float(self.value) * factor

    def getRoundedValue(self, currency=None):
        """returns the value in the appropriate currency rounded to 0.05"""
        value = self.getValue(currency)
        return float(int(math.ceil(value*20)))/20

    def toString(self, currency=None):
        """returns the value in the appropriate currency rounded to 0.05 including the symbol"""
        utility = getUtility(ICurrencyUtility)
        return "%s %0.2f" % (utility.getCurrencySymbol(currency), self.getRoundedValue(currency))
    
    def valueToString(self, currency=None):
        """returns the value in the appropriate currency rounded to 0.05"""
        return "%0.2f" % self.getRoundedValue(currency)
    
    def safeToString(self, currency=None):
        """returns the value in the appropriate currency rounded to 0.05 including the currency-short-name"""
        utility = getUtility(ICurrencyUtility)
        return "%s %0.2f" % (utility.getActiveCurrency(currency), self.getRoundedValue(currency))
