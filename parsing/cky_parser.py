from nltk.tree import Tree
from nltk.grammar import PCFG
from pprint import pprint

class CKYParser(object):
 
    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self._start = grammar.start().symbol()
        productions = grammar.productions()
        uni_prods = [prod for prod in productions if len(prod.rhs()) == 1]
        bin_prods = [prod for prod in productions if len(prod.rhs()) == 2]
        
        uni_prods_dict = {}
        for prod in uni_prods:
            rhs = prod.rhs()[0]
            lhs = prod.lhs().symbol()
            lp = prod.logprob()
            if rhs not in uni_prods_dict:
                uni_prods_dict[rhs] = []

            uni_prods_dict[rhs].append((lhs, lp))

        self._uni_prods_dict = uni_prods_dict 

        bin_prods_dict = {}
        for prod in bin_prods:
            rhs0 = prod.rhs()[0].symbol()
            rhs1 = prod.rhs()[1].symbol()
            lhs = prod.lhs().symbol()
            lp = prod.logprob()
            if (rhs0, rhs1) not in bin_prods_dict:
                bin_prods_dict[(rhs0, rhs1)] = []

            bin_prods_dict[(rhs0, rhs1)].append((lhs, lp))
        
        self._bin_prods_dict = bin_prods_dict 

    def parse(self, sent):
        """Parse a sequence of terminals.
 
        sent -- the sequence of terminals.
        """
        # assert isinstance(sent, list)
        n = len(sent)
        uni_prods_dict = self._uni_prods_dict
        bin_prods_dict = self._bin_prods_dict
        start = self._start
        
        self._pi = {}
        self._bp = {}
        
        # init leaves
        for i, word in enumerate(sent, start=1):
            word_prods = uni_prods_dict[word]
            self._pi[(i, i)] = {}
            self._bp[(i, i)] = {}
            for non_term, lp in word_prods:
                self._pi[(i, i)][non_term] = lp
                self._bp[(i, i)][non_term] = Tree(non_term, [word])        
        
        for span in range(1, n):  # Length of span
            for begin in range(1, n - span + 1):  # Start of span 
                end = begin + span
                self._pi[(begin, end)] = {}
                self._bp[(begin, end)] = {}
                for split in range(begin, end):  # Partition of span
                    s1 = self._pi[(begin, split)]
                    s2 = self._pi[(split + 1, end)] 
                    for rhs1, rhs1_lp in s1.items():
                        for rhs2, rhs2_lp in s2.items():
                            if (rhs1, rhs2) in bin_prods_dict.keys():    
                                lhs_list = bin_prods_dict[(rhs1, rhs2)]
                                for (lhs, lp_lhs) in lhs_list:
                                    lp = rhs1_lp + rhs2_lp + lp_lhs
                                    if lp > self._pi[(begin, end)].get(lhs, float('-inf')):
                                        self._pi[(begin, end)][lhs] = lp
                                        bp_rhs1 = self._bp[(begin, split)][rhs1]
                                        bp_rhs2 = self._bp[(split + 1, end)][rhs2]
                                        t = Tree(lhs, [bp_rhs1, bp_rhs2])
                                        self._bp[(begin, end)][lhs] = t 

        pi_best = self._pi[(1, n)].get(start, float('-inf'))
        bp_best = self._bp[(1, n)].get(start, None)            
        
        return (pi_best, bp_best)
 