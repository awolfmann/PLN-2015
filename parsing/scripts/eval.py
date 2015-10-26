"""Evaulate a parser.

Evaulate a parser.

Usage:
  eval.py -i <file> [-m <m>] [-n <n>]
  eval.py -h | --help

Options:
  -i <file>     Parsing model file.
  -m <m>        Parse only sentences of length <= <m>.
  -n <n>        Parse only <n> sentences (useful for profiling).
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys

from corpus.ancora import SimpleAncoraCorpusReader

from parsing.util import spans


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading model...')
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    print('Loading corpus...')
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    parsed_sents = list(corpus.parsed_sents())
    
    if opts['-m']:
        m = int(opts['-m'])
        parsed_sents = [ s for s in parsed_sents if len(s.leaves()) < m]
    
    if opts['-n']:
        n_len = int(opts['-n'])
        parsed_sents = parsed_sents[:n_len]

    print('Parsing...')
    hits, total_gold, total_model, hits_unl = 0, 0, 0, 0
    n = len(parsed_sents)
    format_str = '{:3.1f}% ({}/{}) (P={:2.2f}%, R={:2.2f}%, F1={:2.2f}%)'
    progress(format_str.format(0.0, 0, n, 0.0, 0.0, 0.0))
    for i, gold_parsed_sent in enumerate(parsed_sents):
        tagged_sent = gold_parsed_sent.pos()

        # parse
        model_parsed_sent = model.parse(tagged_sent)

        # compute labeled scores
        gold_spans = spans(gold_parsed_sent, unary=False)
        model_spans = spans(model_parsed_sent, unary=False)
        hits += len(gold_spans & model_spans)
        total_gold += len(gold_spans)
        total_model += len(model_spans)

        # compute labeled partial results
        prec = float(hits) / total_model * 100
        rec = float(hits) / total_gold * 100
        f1 = 2 * prec * rec / (prec + rec)

        # compute unlabeled scores
        gold_spans_unl = set([(i, j) for n, i, j in gold_spans])
        model_spans_unl = set([(i, j) for n, i, j in model_spans])
        hits_unl += len(gold_spans_unl & model_spans_unl)

        # compute unlabeled partial results
        prec_unl = float(hits_unl) / total_model * 100
        rec_unl = float(hits_unl) / total_gold * 100
        f1_unl = 2 * prec_unl * rec_unl / (prec_unl + rec_unl)

        progress(format_str.format(float(i+1) * 100 / n, i+1, n, prec, rec, f1))

    print('')
    print('Parsed {} sentences'.format(n))
    print('Labeled')
    print('  Precision: {:2.2f}% '.format(prec))
    print('  Recall: {:2.2f}% '.format(rec))
    print('  F1: {:2.2f}% '.format(f1))
    print('Unlabeled')
    print('  Precision: {:2.2f}% '.format(prec_unl))
    print('  Recall: {:2.2f}% '.format(rec_unl))
    print('  F1: {:2.2f}% '.format(f1_unl))