from nltk.tree import Tree


class CKYParser(object):

    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self._start = grammar.start().symbol()
        productions = grammar.productions()

        self._uni_prods_dict = uni_prods_dict = {}
        self._bin_prods_dict = bin_prods_dict = {}

        for prod in productions:
            lhs = prod.lhs().symbol()
            lp = prod.logprob()
            rhs = prod.rhs()
            if len(rhs) == 1:
                rhs = rhs[0]
                if rhs not in uni_prods_dict:
                    uni_prods_dict[rhs] = []

                uni_prods_dict[rhs] += [(lhs, lp)]

            else:
                rhs0 = rhs[0].symbol()
                rhs1 = rhs[1].symbol()
                if (rhs0, rhs1) not in bin_prods_dict:
                    bin_prods_dict[(rhs0, rhs1)] = []

                bin_prods_dict[(rhs0, rhs1)] += [(lhs, lp)]

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
            pi_i = self._pi[(i, i)]
            bp_i = self._bp[(i, i)]
            for (non_term, lp) in word_prods:
                pi_i[non_term] = lp
                bp_i[non_term] = Tree(non_term, [word])

        for span in range(1, n):  # Length of span
            for begin in range(1, n - span + 1):  # Start of span
                end = begin + span
                self._pi[(begin, end)] = {}
                self._bp[(begin, end)] = {}
                pi_begin = self._pi[(begin, end)]
                bp_begin = self._bp[(begin, end)]
                for split in range(begin, end):  # Partition of span
                    pi_s1 = self._pi[(begin, split)]
                    pi_s2 = self._pi[(split + 1, end)]
                    bp_s1 = self._bp[(begin, split)]
                    bp_s2 = self._bp[(split + 1, end)]
                    for rhs1, rhs1_lp in pi_s1.items():
                        for rhs2, rhs2_lp in pi_s2.items():
                            if (rhs1, rhs2) in bin_prods_dict.keys():
                                lhs_list = bin_prods_dict[(rhs1, rhs2)]
                                for (lhs, lp_lhs) in lhs_list:
                                    lp = rhs1_lp + rhs2_lp + lp_lhs
                                    if lp > pi_begin.get(lhs, float('-inf')):
                                        pi_begin[lhs] = lp
                                        bp_rhs1 = bp_s1[rhs1]
                                        bp_rhs2 = bp_s2[rhs2]
                                        t = Tree(lhs, [bp_rhs1, bp_rhs2])
                                        bp_begin[lhs] = t

        pi_best = self._pi[(1, n)].get(start, float('-inf'))
        bp_best = self._bp[(1, n)].get(start, None)

        return (pi_best, bp_best)
