from nltk.tree import Tree
from nltk.grammar import PCFG
from pprint import pprint

class CKYParser(object):
 
    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self._grammar = grammar

    def parse(self, sent):
        """Parse a sequence of terminals.
 
        sent -- the sequence of terminals.
        """
        n = len(sent)
        start = self._grammar.start().symbol()
        self._pi = {}
        self._bp = {}
        lex_prods = [prod for prod in self._grammar.productions() 
                     if prod.is_lexical()]
        non_lex_prods = [prod for prod in self._grammar.productions() 
                         if prod.is_nonlexical()]
        
        # init leaves
        for i, word in enumerate(sent, start=1):
            word_prods = [prod for prod in lex_prods if prod.rhs()[0] == word]
            if len(word_prods) > 0:
                for prod in word_prods:
                    non_term = prod.lhs().symbol()
                    self._pi[(i, i)] = {}
                    self._pi[(i, i)][non_term] = prod.logprob() 
                    self._bp[(i, i)] = {}
                    self._bp[(i, i)][non_term] = Tree(non_term, [word])
        
        for span in range(1, n):  # Length of span
            for begin in range(1, n - span + 1):  # Start of span REVERSED??
                end = begin + span
                self._pi[(begin, end)] = {}
                self._bp[(begin, end)] = {}
                for split in range(begin, end):  # Partition of span
                    for prod in non_lex_prods:
                        lnt = prod.lhs().symbol()
                        rnt1 = prod.rhs()[0].symbol()
                        rnt2 = prod.rhs()[1].symbol()
                        rnt1_lp = self._pi[(begin, split)].get(rnt1, float('-inf'))
                        rnt2_lp = self._pi[(split + 1, end)].get(rnt2, float('-inf'))
                        if  rnt1_lp > float('-inf') and rnt2_lp > float('-inf'):
                            lp = rnt1_lp + rnt2_lp + prod.logprob()

                            if lp > self._pi[(begin, end)].get(lnt, float('-inf')):
                                self._pi[(begin, end)][lnt] = lp
                                bp_rnt1 = self._bp[(begin, split)][rnt1]
                                bp_rnt2 = self._bp[(split + 1, end)][rnt2]
                                t = Tree(lnt, [bp_rnt1, bp_rnt2])
                                self._bp[(begin, end)][lnt] = t 

        pprint(self._pi)
        return (self._pi[(1, n)][start], self._bp[(1, n)][start]) 