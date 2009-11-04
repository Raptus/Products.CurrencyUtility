from Acquisition import aq_inner
from zope.component import getUtility

from zope.i18n import translate

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.instance import memoize

from Products.CMFCore.utils import getToolByName

from Products.CurrencyUtility.interfaces import ICurrencyFactorRegistry
from Products.CurrencyUtility.currencies import currency_list, CURRENCY_NAME
from Products.CurrencyUtility import CurrencyMessageFactory as _

class CurrencyConfigletView(BrowserView):
    """Currency configlet
    """

    errors = {}
    values = {}
    template = ViewPageTemplateFile('currency_configlet.pt')
    properties = ('default','active','autoupdate',)

    def __call__(self):
        self.request.set('disable_border', True)
        
        utility = self.getUtility()
        if self.request.form.has_key('currency_update'):
            utility.update(self.context)
            utils = getToolByName(self.context, 'plone_utils')
            utils.addPortalMessage(_(u'Factors updated'))
        elif self.request.form.has_key('currency_save'):
            self.setProperties()

        props = getToolByName(self.context, 'portal_properties').currency_properties
        for property in self.properties:
            self.values[property] = props.getProperty(property, '')
        
        for currency in currency_list.keys():
            self.values[currency] = utility.getFactor(currency, self.context)
        
        return self.template()
    
    @memoize
    def getCurrencies(self):
        currencies = [{'id': id, 
                       'name': translate(_(currency[CURRENCY_NAME]), context=self.request)} for id, currency in currency_list.items()]
        currencies.sort(cmp=lambda x, y: cmp(x['name'],y['name']))
        return currencies
        
    @memoize
    def getActiveCurrencies(self):
        return [currency for currency in self.getCurrencies() if currency['id'] in self.values['active']]

    def getUtility(self):
        return getUtility(ICurrencyFactorRegistry)

    def setProperties(self):
        context = aq_inner(self.context)
        utils = getToolByName(context, 'plone_utils')
        utility = self.getUtility()
        
        for currency in currency_list.keys():
            if self.request.has_key(currency):
                utility.registerFactor(currency, self.request.get(currency, 1), context)
        
        props = getToolByName(context, 'portal_properties').currency_properties
        for property in self.properties:
            props._setPropValue(property, self.request.get(property, ''))
        utils.addPortalMessage(_(u'Properties saved'))
