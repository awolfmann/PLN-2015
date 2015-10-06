"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import Counter

from corpus.ancora import SimpleAncoraCorpusReader


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/')
    sents = list(corpus.tagged_sents())
    tokens = []
    tagg_list = []
    bow = []
    # quizas con esto alcanza, en vez del for
    # tagged_text = [item for sent in tagged_sents for item in sent]
    for sent in sents:
        words, taggs = zip(*sent)
        tokens += list(words)
        tagg_list += list(taggs)
        bow += sent
    
    tagg_count = Counter(tagg_list)
    top_taggs = tagg_count.most_common(10)

    tokens_count = Counter(tokens)
    tagg_set = set(tagg_list)
    
    for tagg in top_taggs:
        tagg_words = [word[0] for word in bow if tagg[0] == word [1]]
        top_words = Counter(tagg_words).most_common(5)
        print("top words", tagg, top_words) 
    # Falta ambiguedad
    # compute the statistics
    print('sents: {}'.format(len(sents)))
    print('tokens: {}'.format(len(tokens)))
    print('words: {}'.format(len(set(tokens))))
    print('taggs: {}'.format(len(tagg_set)))
    print('taggs most common: {}'.format(top_taggs))

# print('{0}\t{1}\t{2}\t{3}'.format())
# sents: 17379
# tokens: 51
# words: 46483
# tags: 48
