# -*- extra stuff goes here -*-
from zope.i18nmessageid import MessageFactory

rediclasMessageFactory = MessageFactory('collective.rediclas')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
