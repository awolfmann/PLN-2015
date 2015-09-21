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

    def avg_lp(self, eval_sents):
        log_prob = 0.0
        M = 0.0
        for sent in eval_sents:
            M += len(sent) + 1 # counting </s>
            log_prob += self.model.sent_log_prob(sent)

        avg_lp = 1.0/M * log_prob
        return avg_lp

    def cross_entropy(self, eval_sents):
        cross_entropy = - self.avg_lp(eval_sents)
        return cross_entropy

    def perplexity(self, eval_sents):
        cross_entropy = self.cross_entropy(eval_sents)
        perplexity = math.pow(2, cross_entropy)
        return perplexity

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
    evaluator = Eval(model)
    avg_lp = evaluator.avg_lp(eval_sents)
    cross_entropy = evaluator.cross_entropy(eval_sents)
    perplexity = evaluator.perplexity(eval_sents)

    # show results
    print "avg_lp", avg_lp
    print "cross_entropy", cross_entropy
    print "perplexity", perplexity
