# https://docs.python.org/3/library/collections.html
from collections import defaultdict
import math


class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)

        for sent in sents:
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1

    def prob(self, token, prev_tokens=None):
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]
        return float(self.counts[tuple(tokens)]) / self.counts[tuple(prev_tokens)]
 
    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.
 
        tokens -- the n-gram or (n-1)-gram tuple.
        """
 
    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
 
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]
        return float(self.counts[tuple(tokens)]) / self.counts[tuple(prev_tokens)]

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.
 
        sent -- the sentence as a list of tokens.
        """
        sent_prob = 1.0
        for i in range(len(sent)):
            sent_prob *= self.cond_prob(sent[i], sent[i-self.n:i])
        # VER CASOS i<n
        return sent_prob

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.
 
        sent -- the sentence as a list of tokens.
        """
        sent_log_prob = 1.0
        for i in range(len(sent)):
            sent_log_prob *= math.log(self.cond_prob(sent[i], sent[i-self.n:i]))
        # VER CASOS i<n
        return sent_log_prob


class NGramGenerator:
 
    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self.model = model

    def generate_sent(self):
        """Randomly generate a sentence."""
        sent = []
        prev_tokens = []
        i = 0
        while token != "STOP":
            prev_tokens = sent[i - self.model.n : i]
            token = self.generate_token(prev_tokens)
            sent.append(token)
            i += 1

        return sent

    def generate_token(self, prev_tokens=None):
        """
        Randomly generate a token, given prev_tokens.
 
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """

        # calcular cual de todas las palabras del vocabulario es la 
        # mas probable que ocurra dado prev_tokens? 