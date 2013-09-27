# -*- coding: utf-8 -*-
import logging
from zope import interface, schema
from zope.component import getUtility
from zope.formlib import form

from five.formlib import formbase

from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from collective.rediclas import rediclasMessageFactory as _
from collective.rediclas.utils import RedisService

from collective.rediclas.interfaces import ISettingsSchema

logger = logging.getLogger(__name__)


class ITrainSchema(interface.Interface):
    # -*- extra stuff goes here -*-
    do_train = schema.Bool(
        title=u'Train entire corpus in this path',
        description=u'Check to enable training. This can take a while and may make your site unresponsive',
        required=True,
        readonly=False,
        default=False,
        )

    has_subject = schema.Bool(
        title=u'Only Items with Tags',
        description=u'Omit all items without tags. Note that this will not remove earlier classification for items without tags',
        required=True,
        readonly=False,
        default=False,
        )


class Train(formbase.PageForm):
    form_fields = form.FormFields(ITrainSchema)
    label = _(u'Train the Classifier')
    description = _(u'Train the naive Bayes Classifier with current content')

    def __init__(self, context, request):
        super(Train, self).__init__(context, request)
        rs = RedisService()
        if not rs.stopwords:
            IStatusMessage(self.request).addStatusMessage(_(u"No Stopwords defined"), "warn")




    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')


    @form.action('Train')
    def actionTrain(self, action, data):
        if data['do_train']:
            rs = RedisService()
            registry = getUtility(IRegistry)
            settings = registry.forInterface(ISettingsSchema)
            if self.context.portal_type in ['Topic', 'Collection']:
                brains = self.context.queryCatalog()
            else:
                path = '/'.join(self.context.getPhysicalPath())
                brains = self.portal_catalog(path=path,
                                portal_type=settings.content_types)
            i=0
            for brain in brains:
                if data.get('has_subject') and not brain.Subject:
                    continue
                else:
                    if set(brain.Subject).difference(set(settings.tag_blacklist)):
                        #do not process objects with blacklisted keywords only
                        obj = brain.getObject()
                        if rs.train_untrain(obj.UID(), obj.Subject(), obj.SearchableText()):
                            i+=1
                        logger.info('indexing %s' % obj.getId())
            logger.info('indexing complete. Indexed %i items' % i)
        else:
            IStatusMessage(self.request).addStatusMessage(_(u"Check the checkbox to start the training"), "error")

    @form.action('Cancel')
    def actionCancel(self, action, data):
        pass
        # Put the action handler code here
