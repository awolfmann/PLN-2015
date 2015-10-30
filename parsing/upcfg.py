from collections import defaultdict
from nltk.tree import Tree
from nltk.grammar import PCFG, induce_pcfg, Nonterminal

class UPCFG(object):
    """Unlexicalized PCFG.
    """
 
    def __init__(self, parsed_sents):
        """
        parsed_sents -- list of training trees.
        """
        # assert is binarised
        # induce pcfg induce_pcfg(start, productions)
        self.parsed_sents = parsed_sents
        self.productions = []
        starters = defaultdict(int)
        for tree in parsed_sents:
            starters[tree.label()] += 1
            self.productions += list(tree.productions())

        start = max(starters, key=starters.get)
        start = Nonterminal(start)

        self.pcfg = induce_pcfg(start, self.productions)
        assert self.pcfg.is_binarised()

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """

 
    def parse(self, tagged_sent):
        """Parse a tagged sentence.
 
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """