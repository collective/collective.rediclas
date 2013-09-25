from zope import interface, schema
from zope.formlib import form
from five.formlib import formbase

from Products.statusmessages.interfaces import IStatusMessage

from collective.rediclas import rediclasMessageFactory as _
from collective.rediclas.utils import RedisService, simple_preprocess

class IStopwordsSchema(interface.Interface):
    # -*- extra stuff goes here -*-

    stopwords = schema.Text(
        title=u'Stopwords',
        description=u'Stopwords for your language and domain',
        required=True,
        readonly=False,
        default=None,
        )


class Stopwords(formbase.PageForm):
    form_fields = form.FormFields(IStopwordsSchema)
    label = _(u'Stopwords')
    description = _(u'Enter the stopwords for your language/domain here')

    def update(self):
        rs = RedisService()
        stopwords = u' '.join(rs.stopwords)
        self.form_fields.get('stopwords').field.default = stopwords
        super(Stopwords, self).update()


    @form.action('Submit')
    def actionSubmit(self, action, data):
        rs = RedisService()
        rs.stopwords = data['stopwords']
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"), "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(), '@@rediclas-settings.html'))


    @form.action('Cancel')
    def actionCancel(self, action, data):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"), "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(), '@@rediclas-settings.html'))

    @form.action('Train')
    def actionTrain(self, action, data):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"), "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(), '@@rediclas-train.html'))

