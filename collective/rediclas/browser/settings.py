# -*- coding: utf-8 -*-
from zope import interface, schema
from z3c.form import button
from plone.app.registry.browser import controlpanel
from Products.statusmessages.interfaces import IStatusMessage

from collective.rediclas import rediclasMessageFactory as _

from collective.rediclas.interfaces import ISettingsSchema


class Settings(controlpanel.RegistryEditForm):
    schema = ISettingsSchema
    label = _(u'Rediclass Settings')
    description = _(u'Configure Redis')

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"), "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(), self.control_panel_view))

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"), "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(), self.control_panel_view))

    @button.buttonAndHandler(_('Stopwords'), name='stopwords')
    def handleCancel(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"), "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(), '@@rediclas-stopwords.html'))


class SettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = Settings

