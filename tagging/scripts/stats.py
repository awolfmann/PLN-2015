"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import Counter, defaultdict
from itertools import groupby

from corpus.ancora import SimpleAncoraCorpusReader


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/')
    sents = list(corpus.tagged_sents())
    # tokens = []
    # tagg_list = []
    # bow = []
    # for sent in sents:
    #     words, taggs = zip(*sent)
    #     tokens += list(words)
    #     tagg_list += list(taggs)
    #     bow += sent
    
    # tagg_count = Counter(tagg_list)
    # top_taggs = tagg_count.most_common(10)

    # tokens_count = Counter(tokens)
    # tagg_set = set(tagg_list)
    
    # for tagg in top_taggs:
    #     tagg_words = [word[0] for word in bow if tagg[0] == word[1]]
    #     top_words = Counter(tagg_words).most_common(5)
    #     print("top words", tagg, top_words) 

    tagged_text = [item for sent in sents for item in sent]
    tokens = [item[0] for item in tagged_text]
    bow = set(tokens)
    tokens_count = Counter(tokens)

    tags = [item[1] for item in tagged_text]
    tagset = set(tags)
    tag_count = Counter(tags)
    top_tags = tag_count.most_common(10)

    for tag in top_tags:
        tag_words = [item[0] for item in tagged_text if tag[0] == item[1]]
        top_words = Counter(tag_words).most_common(5)
        print("top words", tag, top_words)

    # AMBIGUEDAD
    tagged_text_count = Counter(tagged_text)
    word_tags_count = {}
    for key, value in tagged_text_count.items():
        if key[0] not in word_tags_count:
            word_tags_count[key[0]] = {}

        word_tags_count[key[0]][key[1]] = value

    ambig_dict = defaultdict(int)
    for word, tags in word_tags_count.items():
        ambiguity = len(tags)
        word_ocurrencies = sum(tags.values())
        ambig_dict[ambiguity] += word_ocurrencies
    print(ambig_dict)
    print("sum", sum(ambig_dict.values()))

    # compute the statistics
    print('sents: {}'.format(len(sents)))
    print('tokens: {}'.format(len(tokens)))
    print('words: {}'.format(len(bow)))
    print('tags: {}'.format(len(tagset)))
    print('most common tags: {}'.format(top_tags))

# print('{0}\t{1}\t{2}\t{3}'.format())
# sents: 17379
# tokens: 517268
# words: 46483
# tags: 48
