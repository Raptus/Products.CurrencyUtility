from Acquisition import aq_inner

from zope.component import getUtility

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.instance import memoize

from Products.CurrencyUtility.interfaces import ICurrencyUtility
from Products.CurrencyUtility import CurrencyMessageFactory as _

class CurrencySelectorView(BrowserView):
    """
    """

    __call__ = ViewPageTemplateFile('currency_selector.pt')

    @memoize
    def getCurrencies(self):
        utility = getUtility(ICurrencyUtility)
        currencies = []
        selected_currency = utility.getActiveCurrency()
        active_currencies = utility.getActiveCurrencies()
        for currency in active_currencies:
            currencies.append({'id': currency,
                               'title': _(utility.getCurrencyName(currency)),
                               'selected': (currency == selected_currency)})
        return currencies