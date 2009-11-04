from StringIO import StringIO
from xml.dom import minidom
import urllib
import logging

from persistent import Persistent

from zope.interface import implements
from zope.component import getSiteManager, queryUtility

from Products.CMFPlone.interfaces import IPloneSiteRoot

from Products.CurrencyUtility import currencies
from Products.CurrencyUtility.config import XML_URL, BASE_CURRENCY
from Products.CurrencyUtility.interfaces import ICurrencyUtility, ICurrencyFactorRegistry

from Products.CMFCore.utils import getToolByName
from AccessControl.User import nobody

class Currency(object):
    """currency-utility"""
    implements(ICurrencyUtility)

    context = None

    def getContext(self):
        """returns the context"""
        if self.context is None:
            self.context = getSiteManager()
        return self.context

    def getProperties(self):
        """returns the property-sheet"""
        return getToolByName(self.getContext(), 'portal_properties').currency_properties

    def getBaseCurrency(self):
        """returns the base currency-id"""
        return BASE_CURRENCY

    def getDefaultCurrency(self):
        """returns the default currency-id"""
        props = self.getProperties()
        return props.getProperty('default')

    def getUserCurrency(self):
        """returns the currently logged in users currency"""
        mtool = getToolByName(self.getContext(), 'portal_membership')
        user = mtool.getAuthenticatedMember()
        if user is nobody:
            return None
        try:
            currency = user.getProperty('currency', '')
            if not currency == '':
                return currency
            return None
        except:
            return None

    def getActiveCurrency(self, id=None):
        """returns the current currency"""
        if id is not None:
            return id
        currency = self.getUserCurrency()
        if currency is None:
            currency = self.getDefaultCurrency()
        return currency

    def getCurrencyName(self, id=None):
        """returns the name of the currency"""
        if id is None:
            id = self.getActiveCurrency()
        if id in currencies.currency_list.keys():
            return currencies.currency_list[id][currencies.CURRENCY_NAME]
        return id

    def getCurrencySymbol(self, id=None):
        """returns the symbol of the currency"""
        if id is None:
            id = self.getActiveCurrency()
        if id in currencies.currency_list.keys():
            return currencies.currency_list[id][currencies.CURRENCY_SYMBOL] or id
        return id

    def getCurrencyIsoCode(self, id=None):
        """returns the iso-code of the currency"""
        if id is None:
            id = self.getActiveCurrency()
        if id in currencies.currency_list.keys():
            return currencies.currency_list[id][currencies.CURRENCY_ISOCODE]
        return id

    def getCurrencyFactor(self, id=None):
        """returns the factor of the currency"""
        if id is None:
            id = self.getActiveCurrency()
        registry = queryUtility(ICurrencyFactorRegistry)
        if registry is not None:
            base_factor = registry.getFactor(self.getBaseCurrency(), self.getContext())
            return registry.getFactor(id, self.getContext())/base_factor

    def getCurrencies(self):
        """returns a list of all available currencies (key, info, active)"""
        list = []
        active = self.getActiveCurrencies()
        for currency in currencies.currency_list.keys():
            list.append((currency, currencies.currency_list[currency], (currency in active)))
        list.sort()
        return list

    def getActiveCurrencies(self):
        """returns a list of the active currencies"""
        props = self.getProperties()
        return props.getProperty('active', ())

class CurrencyFactorRegistry(Persistent):
    """currency-factor registry"""
    implements(ICurrencyFactorRegistry)

    __name__ = __parent__ = None

    def update(self, context):
        """updates the currency factors"""
        out = StringIO()
        print >> out, " updating currency factors:"
        try:
            xml = minidom.parse(urllib.urlopen(XML_URL))
            for currency in xml.getElementsByTagName("Cube")[1].getElementsByTagName("Cube"):
                id = currency.getAttribute('currency').lower().decode('utf-8')
                factor = float(currency.getAttribute('rate'))
                self.registerFactor(id, factor, context)
                print >> out, "   factor registered for currency '%s' (%s)" % (id, factor)
        except:
            print >> out, "   parsing xml file at '%s' failed" % XML_URL
        return out.getvalue()

    def getFactor(self, currency, context):
        """returns the registered factor for a currency
           returns 1 if none was registered
        """
        props = getToolByName(context, 'portal_properties').currency_properties
        return props.getProperty('factor_%s' % currency, 1)

    def registerFactor(self, currency, factor, context):
        """register a factor for a currency"""
        props = getToolByName(context, 'portal_properties').currency_properties
        if props.hasProperty('factor_%s' % currency):
            props._setPropValue('factor_%s' % currency, factor)
        else:
            props.manage_addProperty('factor_%s' % currency, factor, 'float')

factorRegistry = CurrencyFactorRegistry()