from collections import namedtuple

from featureforge.feature import Feature

# sent -- the whole sentence.
# prev_tags -- a tuple with the n previous tags.
# i -- the position to be tagged.
History = namedtuple('History', 'sent prev_tags i')


def prev_tags(h):
    return h.prev_tags

def word_lower(h):
    """Feature: current lowercased word.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].lower()


def word_istitle(h):
    """Feature:  is a titlecased word.
    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].istitle()


def word_isupper(h):
    """Feature: is a uppercased word.
    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isupper()


def word_isdigit(h):
    """Feature: is a digit word.
    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isdigit()


def word_isalnum(h):
    """Feature: is an alphanumeric word.
    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isalnum()


def word_isalpha(h):
    """Feature: is an alphabetic word.
    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isalpha()


def word_islower(h):
    """Feature: is a lowercased word.
    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].islower()


def word_isnumeric(h):
    """Feature: is a numeric word.
    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isnumeric()


def word_len(h):
    """Feature: length of the word.
    h -- a history.
    """
    sent, i = h.sent, h.i
    return len(sent[i])


def word_prefix(h, prefix=3):
    """Feature: prefix of the word.
    h -- a history.
    prefix -- length of the prefix
    """
    sent, i = h.sent, h.i
    return sent[i][:prefix]


def word_sufix(h, sufix=3):
    """Feature: sufix of the word.
    h -- a history.
    sufix -- length of the sufix
    """
    sent, i = h.sent, h.i
    return sent[i][-sufix:]

class NPrevTags(Feature):
 
    def __init__(self, n):
        """Feature: n previous tags tuple.
 
        n -- number of previous tags to consider.
        """
        self.n = n
 
    def _evaluate(self, h):
        """n previous tags tuple.
 
        h -- a history.
        """
        sent, i, = h.sent, h.i
        return h.prev_tags[-self.n:]
         
 
class PrevWord(Feature):
 
    def __init__(self, f):
        """Feature: the feature f applied to the previous word.
 
        f -- the feature.
        """
        self.f = f
 
    def _evaluate(self, h):
        """Apply the feature to the previous word in the history.
 
        h -- the history.
        """
        result = None
        if h.i > 0:
            history = History(h.sent, h.prev_tags, h.i-1)
            result = str(self.f(history))
        else:
            result = 'BOS'
        return result
