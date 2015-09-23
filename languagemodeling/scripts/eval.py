"""
Evaulate a language model using the test set.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Language model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from nltk.corpus import gutenberg


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    pkl_file = open(filename, 'rb')
    model = pickle.load(pkl_file)
    pkl_file.close()

    # load data
    sents = gutenberg.sents()
    eval_sents = sents[int(0.9*len(sents)):]

    # evaluate the model
    perplexity = model.perplexity(eval_sents)

    # show results
    print("perplexity", perplexity)
