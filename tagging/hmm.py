import math

class HMM(object):
 
    def __init__(self, n, tagset, trans, out):
        """
        n -- n-gram size.
        tagset -- set of tags.
        trans -- transition probabilities dictionary.
        out -- output probabilities dictionary.
        """
        self.tagset = tagset
        self.n = n
        self.trans = trans
        self.out = out

    def tagset(self):
        """Returns the set of tags.
        """
        return self.tagset

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.
        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        print(self.n-1, prev_tags)
        assert len(prev_tags) == self.n-1
        assert tag in self.tagset
        prev_tags_trans = self.trans[tuple(prev_tags)]
        trans_prob = 0.0
        if tag in prev_tags_trans:
            trans_prob = prev_tags_trans[tag]

        return trans_prob

    def out_prob(self, word, tag):
        """Probability of a word given a tag.
        word -- the word.
        tag -- the tag.
        """
        assert tag in self.tagset
        tag_out = self.out[tag]
        out_prob = 0.0
        if word in tag_out:
            out_prob = tag_out[word]

        return out_prob
 
    def tag_prob(self, y):
        """
        Probability of a tagging.
        Warning: subject to underflow problems.
        y -- tagging.
        """
        tag_prob = 1.0
        prev_tags = ['<s>'] * (self.n - 1)
        for tag in y:
            tag_prob_i = self.trans_prob(tag, prev_tags)
            prev_tags = prev_tags[1:] + [tag]
            tag_prob *= tag_prob_i
        return tag_prob

    def prob(self, x, y):
        """
        Joint probability of a sentence and its tagging.
        Warning: subject to underflow problems.
        x -- sentence.
        y -- tagging.
        """
        assert len(x) == len(y)
        prob = 1.0
        for i, word in enumerate(x):
            out_prob = self.out_prob(word, y[i])
            if out_prob > 0.0:
                prob *= out_prob
            else:
                prob = float('-inf')
                break

        return prob

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.
        y -- tagging.
        """
        log2 = lambda x: math.log(x, 2)
        tag_log_prob = 0.0
        prev_tags = ['<s>'] * (self.n - 1)
        for tag in y:
            tag_prob_i = self.trans_prob(tag, prev_tags)
            prev_tags = prev_tags[1:] + [tag]
            if tag_prob_i > 0.0:
                tag_log_prob += log2(tag_prob_i)
            else:
                tag_log_prob = float('-inf')
                break
        return tag_log_prob

    def log_prob(self, x, y):
        """
        Joint log-probability of a sentence and its tagging.
        x -- sentence.
        y -- tagging.
        """
        assert len(x) == len(y)
        log2 = lambda x: math.log(x, 2)
        log_prob = 0.0
        for i, word in enumerate(x):
            out_prob = self.out_prob(word, y[i])
            if out_prob > 0.0: #CHEQUEAR
                log_prob += log2(out_prob)
            else:
                log_prob = float('-inf')
                break

        return log_prob 

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
        sent -- the sentence.
        """
        tagger = ViterbiTagger(self)
        return tagger.tag(sent)          
 
 
class ViterbiTagger(object):
 
    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
        self.hmm = hmm


    def tag(self, sent):
        """Returns the most probable tagging for a sentence. 
        sent -- the sentence.
        """
        log2 = lambda x: math.log(x, 2)
        self._pi = {
                    0: {
                        tuple(['<s>'] * (self.hmm.n - 1)): 
                            (log2(1.0), []),
            }
        }
        for k, word in enumerate(sent, start=1):
            self._pi[k] = {}
            for n_uple, w in self._pi[k-1].items():
                for tag in self.hmm.tagset:
                    e = self.hmm.out_prob(word, tag)
                    q = self.hmm.trans_prob(tag, n_uple)
                    if e > 0.0 and q > 0.0:
                        log_e = log2(e)
                        log_q = log2(q)
                        site = tuple([n_uple + tuple(tag)][1:])
                        value = w[0] + log_e + log_q
                        prev_tags = w[1]
                        tag_list = prev_tags + [tag]
                        if site in self._pi[k]:
                            prev_value = self._pi[k][site]
                            self._pi[k][site] = (max(value, prev_value), tag_list)
                        else:
                            self._pi[k][site] = (value, tag_list)
                    # else:
                    #     break                    
        return tag_list