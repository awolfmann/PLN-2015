"""
Evaulate a language model using the test set.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Language model file.
  -h --help     Show this screen.
"""
# Metricas:
# Sea x1, .., xn un corpus de evaluacion
# lp = sum de i=1 hasta m de log2 (p(xi))
# avg_lp = 1/M lp a donde M es la cant de tokens:
#     M = suma de i=1 hasta m (ni + 1) (se cuenta </s>)
# cross_entropy = -avg_lp
# perplexity = 2 a la cross_entropy
from docopt import docopt
import pickle
import math

from nltk.corpus import gutenberg

from languagemodeling.ngram import NGram


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
    print "perplexity", perplexity
