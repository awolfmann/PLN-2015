"""Evaulate a tagger.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Tagging model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys

from corpus.ancora import SimpleAncoraCorpusReader


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load the data
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = list(corpus.tagged_sents())

    # tag
    hits, total, hits_unk, total_unk = 0, 0, 0, 0
    n = len(sents)
    for i, sent in enumerate(filter(lambda x: x, sents)):
        word_sent, gold_tag_sent = zip(*sent)
        model_tag_sent = model.tag(word_sent)
        assert len(model_tag_sent) == len(gold_tag_sent), i

        # global score
        hits_sent = [m == g for m, g in zip(model_tag_sent, gold_tag_sent)]
        hits += sum(hits_sent)
        total += len(sent) 
        acc = float(hits) / total

        unk_words_tags = [item for item in sent if model.unknown(item[0])]
        unk_words = [item[0] for item in unk_words_tags]
        model_tag_unk = model.tag(unk_words)
        gold_tag_unk = [item[1] for item in unk_words_tags]
        hits_sent_unk = [m == g for m, g in zip(model_tag_unk, gold_tag_unk)]
        hits_unk += sum(hits_sent_unk)
        total_unk += len(unk_words) 
        progress('{:3.1f}% ({:2.2f}%)'.format(float(i) * 100 / n, acc * 100))

    acc = float(hits) / total
    acc_unk = float(hits_unk) / total_unk
    acc_kno = float(hits - hits_unk) / (total - total_unk)

    print('')
    print('Accuracy: {:2.2f}%'.format(acc * 100))
    print('Accuracy Unknown: {:2.2f}%'.format(acc_unk * 100))
    print('Accuracy known: {:2.2f}%'.format(acc_kno * 100))
    print('hits', hits)
    print('total', total)
    print('hits_unk', hits_unk)
    print('total_unk', total_unk)