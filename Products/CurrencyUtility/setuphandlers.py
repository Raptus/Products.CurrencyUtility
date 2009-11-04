from Products.CMFCore.utils import getToolByName

def setupCurrencyUtility(context):

    # XXX: Since this is run an as extension profile, this shouldn't be
    # needed IMHO, but GS will run this step again if RD has been inspected
    # for an import_steps.xml again.
    if context.readDataFile('currencyutility_various.txt') is None:
        return

    portal = context.getSite()

    # install CronUtility Product
    inst = getToolByName(portal, 'portal_quickinstaller');
    if not inst.isProductInstalled('CronUtility'):
        inst.installProduct('CronUtility')