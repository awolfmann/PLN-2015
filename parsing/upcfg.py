from collections import defaultdict
from nltk.tree import Tree
from nltk.grammar import PCFG, induce_pcfg, Nonterminal

import parsing.util as util
from parsing.cky_parser import CKYParser

class UPCFG(object):
    """Unlexicalized PCFG.
    """
    def __init__(self, parsed_sents, start='sentence'):
        """
        parsed_sents -- list of training trees.
        """
        productions = []
        starters = defaultdict(int)
        for t in parsed_sents:
            t_copy = t.copy(deep=True)
            ut = util.unlexicalize(t_copy)
            ut.chomsky_normal_form()
            ut.collapse_unary(collapsePOS = True)
            starters[ut.label()] += 1
            productions += list(ut.productions())

        start = max(starters, key=starters.get)
        start = Nonterminal(start)

        self.pcfg = induce_pcfg(start, productions)
        assert self.pcfg.is_binarised()

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """
        return self.pcfg.productions()
 
    def parse(self, tagged_sent):
        """Parse a tagged sentence.
 
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        words, tags = zip(*tagged_sent)
        tags = list(tags)
        words = list(words)
        parser = CKYParser(self.pcfg)
        self._parser = parser
        pi, tree = parser.parse(tags)
        if tree is not None:
            tree = util.lexicalize(tree, words)
            tree.un_chomsky_normal_form()
        else:
            subtrees = []
            for word, tag in tagged_sent:
                subtrees.append(Tree(tag, [word]))
            tree = Tree('S', subtrees)
        return tree