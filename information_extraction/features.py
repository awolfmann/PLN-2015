from collections import namedtuple

from featureforge.feature import Feature

History = namedtuple('History', 'sent prev arg1 middle arg2 post')
# sent -- the whole sentence preprocessed.
# prev -- list of previous words to arg1.
# post -- list of post words to arg2.
# middle -- list of words between arg1 and arg2.
# arg1 -- Entity 1
# arg2 -- Entity 2

## CUANDO ES NECESARIO QUE SEAN CLASES QUE HEREDEN DE FEATURE??

def prev_features(h):
    """Feature: return a set of features based on the prev preprocessed words
    h -- a history.
    """    
    prev_words, prev_tags, prev_entities = zip(*h.prev)
    return (list(prev_words), list(prev_tags), list(prev_entities))
# Ver como calcula similaridad entre las listas, 
# las ultimas palabras son las mas importantes ya que son las mas cercanas a arg1
# Ir tomando como features listas q se vayan achicando a izq 
# [hola, que, tal], [que, tal], [tal]

def prev_features_extra(h):
    prevs_words = []
    prevs_tags = []
    prevs_entities = []
    for j in range(len(h.prev)):
        prev = h.prev[j:]
        prev_words, prev_tags, prev_entities = zip(*prev)
        prevs_words += prev_words
        prevs_tags += prev_tags
        prevs_entities += prev_entities
    return (prevs_words, prevs_tags, prevs_entities)

def post_features(h):
    """Feature: return a set of features based on the post preprocessed words
    h -- a history.
    """
    post_words, post_tags, post_entities = zip(*h.post)
    return (list(post_words), list(post_tags), list(post_entities))
# Igual que post pero que se achiquen a derecha

def post_features_extra(h):
    posts_words = []
    posts_tags = []
    posts_entities = []
    for j in range(len(h.post)):
        post = h.post[:j+1]
        post_words, post_tags, post_entities = zip(*post)
        posts_words += post_words
        posts_tags += post_tags
        posts_entities += post_entities

    return (posts_words, posts_tags, posts_entities)

def middle_features(h):
    """Feature: return a set of features based on the post preprocessed words
    h -- a history.
    """
    middle_words, middle_tags, middle_entities = zip(*h.middle)
    return (list(middle_words), list(middle_tags), list(middle_entities))
# Para las del medio se podrian usar bigramas y trigramas


def middle_features_extra(h, n=2):
    """Feature: return a set of features based on the middle preprocessed words
    h -- a history.
    """
    middles_words = []
    middles_tags = []
    middles_entities = []
    for j in range(len(h.middle) - n + 1):
        middle = h.middle[j:j+n]
        middle_words, middle_tags, middle_entities = zip(*middle)
        middles_words += middle_words
        middles_tags += middle_tags
        middles_entities += post_entities

    return (middles_words, middles_tags, middles_entities)


def arg1_features(h):
    """Feature: return a set of features based on the arg1 preprocessed words
    h -- a history.
    """
    arg1_words, arg1_tags, arg1_entities = zip(*h.arg1)
    return (list(arg1_words), list(arg1_tags), list(arg1_entities))


def arg2_features(h):
    """Feature: return a set of features based on the arg1 preprocessed words
    h -- a history.
    """
    arg2_words, arg2_tags, arg2_entities = zip(*h.arg2)
    return (list(arg2_words), list(arg2_tags), list(arg2_entities))



# class NPrevTags(Feature):

#     def __init__(self, n):
#         """Feature: n previous tags tuple.
#         n -- number of previous tags to consider.
#         """
#         self.n = n

#     def _evaluate(self, h):
#         """n previous tags tuple.
#         h -- a history.
#         """
#         return h.prev_tags[-self.n:]


