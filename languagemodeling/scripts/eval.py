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

class Eval(object):
    """docstring for Eval"""
    def __init__(self, model):
        self.model = model

    def avg_lp(self, sents):
        log_prob = 0.0
        M = 0.0
        for sent in sents:
            M += len(sent) + 1
            log_prob += self.model.sent_log_prob(sent)

        avg_lp = 1/M * log_prob
        return avg_lp

    def cross_entropy(self, sents):
        cross_entropy = - self.avg_lp(sents)
        return cross_entropy

    def perplexity(self, sents):
        cross_entropy = self.cross_entropy(sents)
        perplexity = math.pow(2, cross_entropy)
        return perplexity

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    pkl_file = open(filename, 'rb')
    model = pickle.load(pkl_file)
    pkl_file.close()

    # evaluate the model
    evaluator = Eval(model)
    perplexity = evaluator.perplexity(eval_sents)
    cross_entropy = evaluator.cross_entropy(eval_sents)

    # show results
    print "perplexity", perplexity
    print "cross_entropy", cross_entropy
