"""Train a sequence tagger.

Usage:
  train.py [-m <model>] -o <file> [-n <n>] 
  train.py -h | --help

Options:
  -m <model>    Model to use [default: base]:
                  base: Baseline
                  hmm: ML hmm
                  memm: MEMM
  -o <file>     Output model file.
  -h --help     Show this screen.
  -n            Order of the model
"""
from docopt import docopt
import pickle

from corpus.ancora import SimpleAncoraCorpusReader
from tagging.baseline import BaselineTagger
from tagging.hmm import HMM, MLHMM
from tagging.memm import MEMM


models = {
    'base': BaselineTagger,
    'hmm' : MLHMM,
    'memm' : MEMM, 
}


if __name__ == '__main__':
    opts = docopt(__doc__)
    print(opts)

    # load the data
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = list(corpus.tagged_sents())

    # train the model
    model = None
    if opts['-m'] != 'base':
        n = int(opts['<n>'])

        print('N', n)
        model = models[opts['-m']](n, sents)
    else:
        model = models[opts['-m']](sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
