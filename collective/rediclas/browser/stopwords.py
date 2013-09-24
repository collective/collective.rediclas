from zope import interface, schema
from zope.formlib import form
from five.formlib import formbase
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from collective.rediclas import rediclasMessageFactory as _

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

    @form.action('Submit')
    def actionSubmit(self, action, data):
        pass
        # Put the action handler code here

    @form.action('Cancel')
    def actionCancel(self, action, data):
        pass
        # Put the action handler code here



