"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import Counter, defaultdict

from corpus.ancora import SimpleAncoraCorpusReader


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/')
    sents = list(corpus.tagged_sents())

    tagged_text = [item for sent in sents for item in sent]
    tokens = [item[0] for item in tagged_text]
    bow = set(tokens)
    tokens_count = Counter(tokens)

    tags = [item[1] for item in tagged_text]
    tagset = set(tags)
    tag_count = Counter(tags)
    top_tags = tag_count.most_common(10)

    # compute the statistics
    print('sents: {}'.format(len(sents)))
    print('tokens: {}'.format(len(tokens)))
    print('words: {}'.format(len(bow)))
    print('tags: {}'.format(len(tagset)))

    print('Top 10 tags statistics')
    print('Tag\tFrecuency\tPercentage')
    for tag in top_tags:
        print('{}\t{}\t{:2.2f}%'.
              format(tag[0], tag[1], float(tag[1]) / len(tokens) * 100.0))

    print('Top 5 words per tag')
    for tag in top_tags:
        tag_words = [item[0] for item in tagged_text if tag[0] == item[1]]
        top_words = Counter(tag_words).most_common(5)
        top_words = [word[0] for word in top_words]
        print(tag[0] + '\t', end='')
        print('\t'.join(top_words))

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
    print('AMBIGUEDAD')
    for level, freq in ambig_dict.items():
        print('{}\t{}\t{:2.2f}%'
              .format(level, freq, float(freq)/len(tokens) * 100.0))
