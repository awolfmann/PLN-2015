"""Train an n-gram model.

Usage:
  train.py -n <n> -o <file>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -o <file>     Output model file.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
                  addone: N-grams with add-one smoothing.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from nltk.corpus import gutenberg

from languagemodeling.ngram import NGram


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    sents = gutenberg.sents()
    train_sents = sents[:int(0.9*len(sents))]
    eval_sents = sents[int(0.9*len(sents)):]
    # train_sents = [["hola", "ariel", "mauricio", "wolfmann"],
    #     ["chau", "ariel", "mauricio"] ]
    # train the model
    n = int(opts['-n'])
    if '-m' in opts and opts['-m'] == "addone":
        model = AddOneNGram(n, train_sents)
    else: 
        model = NGram(n, train_sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
