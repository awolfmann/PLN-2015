import math
from math import log2
from collections import Counter, defaultdict

class HMM(object):

    def __init__(self, n, tagset, trans, out):
        """
        n -- n-gram size.
        tagset -- set of tags.
        trans -- transition probabilities dictionary.
        out -- output probabilities dictionary.
        """
        self._tagset = tagset
        self.n = n
        self.trans = trans
        self.out = out

    def tagset(self):
        """Returns the set of tags.
        """
        return self._tagset

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.
        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        assert len(prev_tags) == self.n-1
        # assert tag in self.tagset
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
        assert tag in self.tagset(), tag
        assert tag in self.out, tag
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
        y += ['</s>']  # add stop tag to the tagging
        for tag in y:
            tag_prob_i = self.trans_prob(tag, prev_tags)
            prev_tags = (prev_tags + [tag])[1:]
            tag_prob *= tag_prob_i
        return tag_prob

    def prob(self, x, y):
        """
        Joint probability of a sentence and its tagging.
        Warning: subject to underflow problems.
        x -- sentence.
        y -- tagging.
        """
        prob = 1.0
        tag_prob = self.tag_prob(y)
        for i, word in enumerate(x):
            out_prob = self.out_prob(word, y[i])
            if out_prob > 0.0:
                prob *= out_prob
            else:
                prob = float('-inf')
                break
        prob *= tag_prob
        
        return prob

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.
        y -- tagging.
        """
        log2 = lambda x: math.log(x, 2)
        tag_log_prob = 0.0
        prev_tags = ['<s>'] * (self.n - 1)
        # y += ['</s>']
        for tag in y:
            tag_prob_i = self.trans_prob(tag, prev_tags)
            prev_tags = (prev_tags + [tag])[1:]
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
        log2 = lambda x: math.log(x, 2)
        log_prob = 0.0
        tag_log_prob = self.tag_log_prob(y)
        for i, word in enumerate(x):
            out_prob = self.out_prob(word, y[i])
            if out_prob > 0.0:
                log_prob += log2(out_prob)
            else:
                log_prob = float('-inf')
                break
        log_prob += tag_log_prob
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
        self._pi = {
                    0: {
                        tuple(['<s>'] * (self.hmm.n - 1)): 
                            (log2(1.0), []),
            }
        }
        tag_list = []
        for k, word in enumerate(sent, start=1):
            self._pi[k] = {}
            for tag in self.hmm.tagset():
                e = self.hmm.out_prob(word, tag)
                if e > 0.0:
                    log_e = log2(e)
                    for n_uple, (lp, prev_tags) in self._pi[k-1].items():
                        q = self.hmm.trans_prob(tag, n_uple)
                        if q > 0.0:
                            log_q = log2(q)
                            site = (n_uple + (tag,))[1:]
                            value = lp + log_e + log_q
                            tag_list = prev_tags + [tag]
                            if site in self._pi[k]:
                                prev_value = self._pi[k][site]
                                if value > prev_value[0]:
                                    self._pi[k][site] = (value, tag_list)
                            else:
                                self._pi[k][site] = (value, tag_list)                   

        max_lp = float('-inf')
        best_tag = None
        for prev_tags, (value, tag_list) in self._pi[len(sent)].items():
            p = self.hmm.trans_prob('</s>', prev_tags)
            if p > 0.0:
                lp = log2(p) + value
                if lp > max_lp:
                    max_lp = lp
                    best_tag = tag_list

        return best_tag


class MLHMM(HMM):
 
    def __init__(self, n, tagged_sents, addone=True):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """
        self.n = n
        self.addone = addone
        self._tcount = tcount = defaultdict(int)
        tagged_text = [item for sent in tagged_sents for item in sent]
        self.bow = set([item[0] for item in tagged_text])
        all_tags = []
        for sent in filter(lambda x: x, tagged_sents):
            words, tags = zip(*sent)
            prev_tags = ['<s>'] * (self.n - 1)
            prev_tags = tuple(prev_tags)
            tags = prev_tags + tags + ('</s>',)
            all_tags += list(tags)
            for i in range(len(tags) - n + 1):
                n_tags = tags[i: i + n]
                tcount[n_tags] += 1
                tcount[n_tags[:-1]] += 1

        self.tag_counts = Counter(all_tags)
        self._tagset = set(all_tags)
        self.words_tagged_count = Counter(tagged_text)

    def tcount(self, tags):
        """Count for an k-gram for k <= n.
        tags -- the k-gram tuple.
        """
        assert len(tags) <= self.n
        tcount = 0
        if tags in self._tcount:
            tcount = self._tcount[tags] 
        return tcount

    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
        return w not in self.bow

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.
        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        assert tag in self.tagset()
        trans_prob = 0.0
        tags = tuple(prev_tags) + (tag,)
        if self.addone:
            tcount_tags = float(self.tcount(tags)) + 1.0
            tcount_prev_tags = self.tcount(tuple(prev_tags)) + len(self.tagset()) 
            trans_prob =  tcount_tags / tcount_prev_tags
            
        elif self.tcount(tuple(prev_tags)) > 0.0:
            trans_prob = float(self.tcount(tags)) / self.tcount(tuple(prev_tags))
        
        return trans_prob


    def out_prob(self, word, tag):
        """Probability of a word given a tag.
        word -- the word.
        tag -- the tag.
        """
        assert tag in self.tagset()
        out_prob = 0.0
        if self.unknown(word):
            out_prob = 1.0 / len(self.bow)
        else:
            trans_count  = self.words_tagged_count[(word, tag)]
            tag_count = self.tag_counts[tag]
            if tag_count > 0.0:
                out_prob = trans_count / float(tag_count)

        return out_prob