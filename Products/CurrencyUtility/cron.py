from zope.interface import implements
from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName

from Products.CronUtility.interfaces import ICron

from Products.CurrencyUtility.interfaces import ICurrencyFactorRegistry

class CurrencyCron(object):
    """the cron used for updating the currency factors"""
    implements(ICron)

    def active(self, datetime):
        return datetime.hour in (1, 7, 13, 19) and datetime.minute < 5

    def run(self, context):
        props = getToolByName(context, 'portal_properties').currency_properties
        if props.getProperty('autoupdate', 0):
            registry = queryUtility(ICurrencyFactorRegistry)
            if registry is None:
                return u"factor-registry not found"
            return registry.update(context)
        return u"auto updating disabled"