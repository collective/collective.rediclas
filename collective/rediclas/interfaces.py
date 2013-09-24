from zope import interface, schema
# -*- Additional Imports Here -*-
from collective.rediclas import rediclasMessageFactory as _


class ICollectiveRediclasLayer(interface.Interface):
    """ A layer specific to this product.
        Is registered using browserlayer.xml
    """

class ISettingsSchema(interface.Interface):
    # -*- extra stuff goes here -*-

    redis_host = schema.TextLine(
        title=u'Redis Host',
        description=u'Redis Hostname',
        required=True,
        readonly=False,
        default=u'localhost',
        )

    redis_port = schema.Int(
        title=u'Redis Port',
        description=u'Port on which Redis listens',
        required=True,
        readonly=False,
        default=6379,
        )

    redis_db = schema.Int(
        title=u'Redis Database',
        description=u'The Redis db to connect to',
        required=True,
        readonly=False,
        default=0,
        )

    content_types = schema.List(
        title = _(u'Content types'),
        description = _(u"""Content types to be classified)"""),
        required = False,
        default = [u"File", u"Document", u'News Item',],
        value_type = schema.Choice(title=_(u"Content types"),
                    source="plone.app.vocabularies.ReallyUserFriendlyTypes"))

    tag_blacklist = schema.List(
        title = _(u'Tags not to be classified'),
        description = _(u"""These Tags will not be passed to the classifier"""),
        required = False,
        default = [],
        value_type = schema.Choice(title=_(u"Tags not to be classified"),
                    description = _(u"""These Tags will not be passed to the classifier"""),
                    source="plone.app.vocabularies.Keywords"))
