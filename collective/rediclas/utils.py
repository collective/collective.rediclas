# -*- coding: utf-8 -*-
import logging
import re
import redis
import redisbayes
import unicodedata

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from .interfaces import ISettingsSchema
logger = logging.getLogger(__name__)


PAT_ALPHABETIC = re.compile('(((?![\d])\w)+)', re.UNICODE)

def deaccent(text):
    """
    Remove accentuation from the given string. Input text is either a unicode string or utf8 encoded bytestring.

    Return input string with accents removed, as unicode.

    >>> deaccent("Šéf chomutovských komunistů dostal poštou bílý prášek")
    u'Sef chomutovskych komunistu dostal postou bily prasek'
    """
    if not isinstance(text, unicode):
        text = unicode(text, 'utf8') # assume utf8 for byte strings, use default (strict) error handling
    norm = unicodedata.normalize("NFD", text)
    result = u''.join(ch for ch in norm if unicodedata.category(ch) != 'Mn')
    return unicodedata.normalize("NFC", result)


def tokenize(text, lowercase=False, deacc=False, errors="strict"):
    """
    Iteratively yield tokens as unicode strings, optionally also lowercasing them
    and removing accent marks.

    Input text may be either unicode or utf8-encoded byte string.

    The tokens on output are maximal contiguous sequences of alphabetic
    characters (no digits!).

    >>> list(tokenize('Nic nemůže letět rychlostí vyšší, než 300 tisíc kilometrů za sekundu!', deacc = True))
    [u'Nic', u'nemuze', u'letet', u'rychlosti', u'vyssi', u'nez', u'tisic', u'kilometru', u'za', u'sekundu']
    """
    if not isinstance(text, unicode):
        text = unicode(text, encoding='utf8', errors=errors)
    if lowercase:
        text = text.lower()
    if deacc:
        text = deaccent(text)
    for match in PAT_ALPHABETIC.finditer(text):
        yield match.group()


def simple_preprocess(doc, deacc=True):
    """
    Convert a document into a list of tokens.

    This lowercases, tokenizes, stems, normalizes etc. -- the output are final,
    utf8 encoded strings that won't be processed any further.
    """
    tokens = [token.encode('utf8') for token in tokenize(doc, lowercase=True, deacc=deacc, errors='ignore')
            if 2 <= len(token) <= 15 and not token.startswith('_')]
    return tokens


class RedisService(object):

    deaccent = True
    _PREFIX = 'c.rediclas.'

    def __init__(self):
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISettingsSchema)
        rh = self.settings.redis_host
        rp = self.settings.redis_port
        rd = self.settings.redis_db
        self.redis_server = redis.Redis(host=rh, port=rp, db=rd)
        self.redis_bayes = redisbayes.RedisBayes(self.redis_server,
            prefix=self._PREFIX + 'bayes:', tokenizer=self.tokenizer)


    def tokenizer(self, text):
        tokens = simple_preprocess(text,
                deacc=self.deaccent)
        return (token for token in tokens if not token in self.stopwords)

    @property
    def stopwords(self):
        return self.redis_server.smembers(self._PREFIX +'stopwords')

    @stopwords.setter
    def stopwords(self, text):
        self.redis_server.delete(self._PREFIX +'stopwords')
        tokens = simple_preprocess(text, deacc=self.deaccent)
        for token in tokens:
           self.redis_server.sadd(self._PREFIX + 'stopwords', token)

    def train_untrain(self, uid, tags, text):
        old_tags = self.redis_server.smembers(self._PREFIX + 'document:' + uid)
        if not uid:
            raise ValueError
        if not text:
            raise ValueError
        for tag in tags:
            if tag in old_tags:
                continue
            else:
                if self.settings.tag_blacklist:
                    if tag not in self.settings.tag_blacklist:
                        self.redis_server.sadd(self._PREFIX +'document:'+uid, tag)
                        self.redis_bayes.train(tag, text)
                else:
                    self.redis_server.sadd(self._PREFIX +'document:'+uid, tag)
                    self.redis_bayes.train(tag, text)
        for old_tag in old_tags:
            if old_tag in tags:
                continue
            else:
                self.redis_server.srem(self._PREFIX + 'document:'+uid, old_tag)
                self.redis_bayes.untrain(tag, text)
        return self.redis_server.smembers(self._PREFIX + 'document:' + uid)

    def classify(self, text):
        scores = self.redis_bayes.score(text)
        #xxx
        return scores
