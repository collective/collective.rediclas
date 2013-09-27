from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from collective.rediclas import rediclasMessageFactory as _
from collective.rediclas.utils import RedisService



class IClassifyView(Interface):
    """
    Classify view interface
    """


class ClassifyView(BrowserView):
    """
    Classify browser view
    """
    implements(IClassifyView)
    template = ViewPageTemplateFile('classifyview.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_keywords(self):
        rs = RedisService()
        kws = rs.classify(self.context.SearchableText())
        import ipdb; ipdb.set_trace()
        return kws


    def __call__(self):
        form = self.request.form
        if 'form.button.save' in form:
            if form.get('keyword'):
                rs = RedisService()
                self.context.setSubject(form['keyword'])
                rs.train_untrain(self.context.UID(), self.context.Subject(),
                        self.context.SearchableText())
                self.request.response.redirect(self.context.absolute_url() + '/view')
                return ''
        elif 'form.button.cancel' in form:
            self.request.response.redirect(self.context.absolute_url() + '/view')
            return ''
        elif 'form.button.reindex' in form:
            if rs.train_untrain(self.context.UID(), self.context.Subject(),
                    self.context.SearchableText()):
                status = _(u"Bayes Filter trained")
                IStatusMessage(self.request).addStatusMessage(status,
                    type='info')
        return self.template()

