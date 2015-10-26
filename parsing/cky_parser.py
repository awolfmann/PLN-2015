from nltk.tree import Tree
from nltk.grammar import PCFG


class CKYParser(object):
 
    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self.grammar = grammar

    def parse(self, sent):
        """Parse a sequence of terminals.
 
        sent -- the sequence of terminals.
        """
        n = len(sent)
        self._pi = {}
        self._bp = {}
        lex_prods = [for prod in self.grammmar.productions() 
                     if prod.is_lexical()]
        non_lex_prods = [for prod in self.grammmar.productions() 
                         if prod.is_nonlexical()]
        
        # init leaves
        for prod in lex_prods:
            non_term = prod.lhs()
            term = prod.rhs()[0]
            pos = [i for i, word sentence if term == word]
            if len(pos) > 0:
                for p in pos:
                    self._pi[(p, p)] = {}
                    self._pi[(p, p)][non_term] = prod.logprob() 
                    self._bp[(p, p)] = {}
                    tree = Tree.fromstring('(' + non_term + ' ' + term + ')')
                    self._bp[(p, p)][non_term] = tree
        
        for span in range(1, n + 1):  # Length of span
            for begin in range(n - span + 1):  # Start of span REVERSED??
                end = begin + span
                self._pi[(begin, end)] = {}
                self._bp[(begin, end)] = {}
                for split in range(begin + 1, end):  # Partition of span
                    for prod in non_lex_prods:
                        lnt = prod.lhs()
                        rnt1 = prod.rhs()[0]
                        rnt2 = prod.rhs()[1]
                        rnt1_p = self._pi[(begin, split)][rnt1]
                        rnt2_p = self._pi[(split, end)][rnt2]
                        lp = rnt1_p * rnt2_p * prod.logprob()
                        if lnt in self._pi[(begin, end)]:
                            if lp > self._pi[(begin, end)][lnt]:
                                self._pi[(begin, end)][lnt] = lp
                                bp_rnt1 = self._bp[(begin, split)][rnt1].pformat()
                                bp_rnt2 = self._bp[(begin, split)][rnt2].pformat() 
                                t = Tree.fromstring('(' + lnt + bp_rnt1 + bp_rnt2 + ')')
                                self._bp[(begin, end)][lnt] = t
                        else: 
                            self._pi[(begin, end)][lnt] = lp
                            bp_rnt1 = self._bp[(begin, split)][rnt1].pformat()
                            bp_rnt2 = self._bp[(begin, split)][rnt2].pformat() 
                            t = Tree.fromstring('(' + lnt + bp_rnt1 + bp_rnt2 + ')')
                            self._bp[(begin, end)][lnt] = t

        return (self._pi, self._bp) 