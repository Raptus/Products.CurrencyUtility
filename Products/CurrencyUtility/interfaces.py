from zope import interface

class ICurrencyUtility(interface.Interface):
    """currency-utility"""

    def getContext():
        """returns the context"""

    def getProperties():
        """returns the property-sheet"""

    def getBaseCurrency():
        """returns the base currency-id"""

    def getDefaultCurrency():
        """returns the default currency-id"""

    def getUserCurrency():
        """returns the currently logged in users currency"""

    def getActiveCurrency():
        """returns the current currency"""

    def getCurrencyName(id=None):
        """returns the name of the currency"""

    def getCurrencySymbol(id=None):
        """returns the symbol of the currency"""

    def getCurrencyIsoCode(id=None):
        """returns the iso-code of the currency"""

    def getCurrencyFactor(id=None):
        """returns the factor of the currency"""

    def getCurrencies():
        """returns a list of all available currencies (key, info, active)"""

    def getActiveCurrencies():
        """returns a list of the active currencies"""

class ICurrencyFactorRegistry(interface.Interface):
    """currency-factor registry"""

    def update():
        """updates the currency factors"""

    def getFactor(currency):
        """returns the registered factor for a currency
           returns 1 if none was registered
        """

    def registerFactor(currency, factor):
        """register a factor for a currency"""

class ICurrencyAware(interface.Interface):
    """helper class to convert values between currencies"""

    currency = interface.Attribute(
        """string: the id of the target currency""")

    value = interface.Attribute(
        """float: the value in the base-currency""")
        
    def getCurrencySymbol():
        """returns the currency symbol"""

    def getValue(currency=None):
        """returns the value in the appropriate currency"""

    def getRoundedValue(currency=None):
        """returns the value in the appropriate currency rounded to 0.01"""

    def toString():
        """returns the value in the appropriate currency rounded to 0.01 including the symbol"""
    
    def valueToString():
        """returns the value in the appropriate currency rounded to 0.01"""
    
    def safeToString():
        """returns the value in the appropriate currency rounded to 0.01 including the currency-short-name"""
