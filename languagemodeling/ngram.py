# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log2
import random
import operator


class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self._n = n
        self._counts = counts = defaultdict(int)
        self._len_v = 0
        words = []
        for sent in sents:
            init_markers = ['<s>' for _ in range(n - 1)]
            final_marker = ['</s>']
            sent_marked = init_markers + sent + final_marker
            for i in range(len(sent_marked) - n + 1):
                ngram = tuple(sent_marked[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1
            words += sent
        vocab = set(words)
        vocab.add('</s>')
        self._len_v = len(vocab)

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self._n
        if not prev_tokens:
            prev_tokens = tuple()
        assert len(prev_tokens) == n - 1
        prev_tokens = tuple(prev_tokens)

        tokens = prev_tokens + (token,)
        prev_count = self.count(prev_tokens)
        cond_prob = 0.0
        if prev_count > 0:
            cond_prob = float(self.count(tokens)) / prev_count

        return cond_prob

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.
        tokens -- the n-gram or (n-1)-gram tuple.
        """
        return self._counts.get(tokens, 0)

    def sent_prob(self, sent):
        """Probability of a sentence.
        Warning: subject to underflow problems.
        sent -- the sentence as a list of tokens.
        """
        n = self._n
        init_markers = ['<s>' for _ in range(n - 1)]
        final_marker = ['</s>']
        sent_marked = init_markers + sent + final_marker
        sent_prob = 1.0

        for i in range(n - 1, len(sent_marked)):
            sent_prob *= self.cond_prob(sent_marked[i], sent_marked[i-n+1:i])
        return sent_prob

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.
        sent -- the sentence as a list of tokens.
        """
        n = self._n
        init_markers = ['<s>' for _ in range(n - 1)]
        final_marker = ['</s>']
        sent_marked = init_markers + sent + final_marker
        sent_log_prob = 0.0

        for i in range(n - 1, len(sent_marked)):
            cond_prob = self.cond_prob(sent_marked[i], sent_marked[i-n+1:i])
            if cond_prob > 0.0:
                sent_log_prob += log2(cond_prob)
            else:
                sent_log_prob = float('-inf')
                break

        return sent_log_prob

    def avg_lp(self, eval_sents):
        log_prob = 0.0
        M = 0.0
        for sent in eval_sents:
            M += len(sent) + 1  # counting </s>
            sent_lp = self.sent_log_prob(sent)
            if sent_lp > float('-inf'):
                log_prob += sent_lp
            else:
                log_prob = float('-inf')
                break

        avg_lp = 1.0/M * log_prob
        return avg_lp

    def cross_entropy(self, eval_sents):
        cross_entropy = - self.avg_lp(eval_sents)
        return cross_entropy

    def perplexity(self, eval_sents):
        cross_entropy = self.cross_entropy(eval_sents)
        perplexity = pow(2, cross_entropy)
        return perplexity


class NGramGenerator(object):

    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self.model = model
        def_dict = lambda: defaultdict(int)
        self.probs = defaultdict(def_dict)
        self.sorted_probs = defaultdict(def_dict)

        for ngram in model._counts.keys():
            if len(ngram) == model._n:
                prev_tokens = ngram[:-1]
                token = ngram[-1]
                self.probs[prev_tokens][token] = \
                    model.cond_prob(token, list(prev_tokens))

        for key, value in self.probs.items():
            self.sorted_probs[key] = \
                sorted(value.items(), key=lambda x: (-x[1], x[0]))

        self.probs = dict(self.probs)
        self.sorted_probs = dict(self.sorted_probs)

    def generate_sent(self):
        """Randomly generate a sentence."""
        sent = []
        prev_tokens = ['<s>' for _ in range(self.model._n - 1)]
        token = self.generate_token(prev_tokens)
        sent = [token]
        while token != "</s>":
            prev_tokens = (prev_tokens + [token])[1:]
            token = self.generate_token(prev_tokens)
            sent.append(token)

        # ignore the "</s>"
        return sent[:-1]

    def generate_token(self, prev_tokens=None):
        """
        Randomly generate a token, given prev_tokens.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.model._n
        if not prev_tokens:
            prev_tokens = ()
        prev_tokens = tuple(prev_tokens)
        assert len(prev_tokens) == n - 1
        val = random.random()
        generated_token = None
        token_prob_list = self.sorted_probs[prev_tokens]
        acum_prob = 0.0
        for (token, prob) in token_prob_list:
            acum_prob += prob
            if val <= acum_prob:
                generated_token = token
                break

        assert generated_token is not None
        return generated_token


class AddOneNGram(NGram):

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self._n
        if not prev_tokens:
            prev_tokens = ()
        assert len(prev_tokens) == n - 1
        prev_tokens = tuple(prev_tokens)
        tokens = prev_tokens + (token,)
        tokens_count = float(self.count(tokens) + 1)
        prev_count = self.count(prev_tokens) + self._len_v
        return tokens_count / prev_count

    def V(self):
        """Size of the vocabulary.
        """
        return self._len_v


class InterpolatedNGram(NGram):

    def __init__(self, n, sents, gamma=None, addone=True):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        gamma -- interpolation hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        assert n > 0
        self._n = n
        self._counts = counts = defaultdict(int)
        self._len_v = 0
        self._addone = addone

        if gamma is not None:
            self._gamma = gamma
        else:
            held_out = sents[int(0.9*len(sents)):]
            sents = sents[:int(0.9*len(sents))]
            self._gamma = self.estimate_gamma(held_out)

        words = []
        for sent in sents:
            init_markers = ['<s>' for _ in range(n - 1)]
            final_marker = ['</s>']
            sent_marked = init_markers + sent + final_marker
            for i in range(len(sent_marked) - n + 1):
                ngram = tuple(sent_marked[i: i + n])
                counts[ngram] += 1
                for j in range(1, n + 1):
                    counts[ngram[j:]] += 1
            counts[('<s>',)] += 1
            # The first unigram is ignored in the recursion
            words += sent_marked
        vocab = set(words)
        vocab.add('</s>')
        self._len_v = len(vocab)
        self._len_w = len(words)

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self._n
        if not prev_tokens:
            prev_tokens = ()
        prev_tokens = tuple(prev_tokens)
        assert len(prev_tokens) == n - 1

        sum_lamdas = 0.0
        cond_prob = 0.0

        for i in range(n):
            lamda = self.lamda(i + 1, sum_lamdas, prev_tokens[i:])
            sum_lamdas += lamda
            prev_count = self.count(prev_tokens[i:])
            tokens_count = float(self.count(prev_tokens[i:] + (token,)))

            if len(prev_tokens[i:]) == 0 and self._addone:  # Unigram
                tokens_count += 1.0
                prev_count += self._len_v
            if lamda > 0.0 and prev_count > 0:
                c = tokens_count / prev_count
                cond_prob += lamda * c

        return cond_prob

    def lamda(self, i, sum_lamdas, tokens):
        """calculate the ith lambda"""
        assert isinstance(tokens, tuple), tokens
        lamda = 0.0
        if i < self._n:
            tokens_count = float(self.count(tokens))
            prev_count = tokens_count + self._gamma
            c = tokens_count / prev_count
            lamda = (1.0 - sum_lamdas) * c
        else:
            lamda = 1.0 - sum_lamdas

        return lamda

    def estimate_gamma(self, held_out):
        gammas = [pow(10, x) for x in range(5)]

        perplexities = {}
        for gamma in gammas:
            self._gamma = gamma
            perp = self.perplexity(held_out)
            perplexities[gamma] = perp

        best_gamma = min(perplexities.items(), key=operator.itemgetter(1))[0]

        return best_gamma


class BackOffNGram(NGram):

    def __init__(self, n, sents, beta=None, addone=True):
        """
        Back-off NGram model with discounting as described by Michael Collins.
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        beta -- discounting hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        assert n > 0
        self._n = n
        self._counts = counts = defaultdict(int)
        self._len_v = 0
        self._addone = addone
        self._alpha = {}
        self._denom = {}
        self._A = defaultdict(set)

        if beta is not None:
            self._beta = beta
        else:
            held_out = sents[int(0.9*len(sents)):]
            sents = sents[:int(0.9*len(sents))]

        vocab = ['</s>']
        for sent in sents:
            init_markers = ['<s>' for _ in range(n - 1)]
            final_marker = ['</s>']
            sent_marked = init_markers + sent + final_marker

            for i in range(len(sent_marked) - n + 1):
                ngram = tuple(sent_marked[i: i + n])
                for j in range(n + 1):
                    counts[ngram[j:]] += 1
                # precalculate A
                self._A[ngram[:-1]].add(ngram[-1])

            for i in range(1, n):
                counts[('<s>',) * i] += 1

            vocab += sent

        self._counts = dict(self._counts)
        self._vocab = set(vocab)
        self._len_vocab = len(self._vocab)
        self._A = dict(self._A)

        if beta is None:
            self._beta = self.estimate_beta(held_out)

    def A(self, tokens):
        """
        Set of words with counts > 0 for a k-gram with 0 < k < n.
        tokens -- the k-gram tuple.
        """
        # assert len(tokens) < self._n
        A = None
        # assert tokens in self._A, tokens
        if tokens in self._A:
            A = self._A[tokens]
        else:
            A = self.compute_A(tokens)
            self._A[tokens] = A
        return A

    def compute_A(self, tokens):
        """
        Compute the set of words with counts > 0
        for a k-gram with 0 < k < n.
        tokens -- the k-gram tuple.
        """
        # assert isinstance(tokens, tuple), tokens
        A = {word for word in self._vocab
             if self.count(tokens + (word,)) > 0}
        return A

    def alpha(self, tokens):
        """
        Missing probability mass
        for a k-gram with 0 < k < n.
        tokens -- the k-gram tuple.
        """
        # assert isinstance(tokens, tuple), tokens
        alpha = None
        if tokens in self._alpha:
            alpha = self._alpha[tokens]
        else:
            alpha = self.compute_alpha(tokens)
            self._alpha[tokens] = alpha

        return alpha

    def compute_alpha(self, tokens):
        """
        Compute the missing probability mass
        for a k-gram with 0 < k < n.
        tokens -- the k-gram tuple.
        """
        # assert isinstance(tokens, tuple), tokens
        token_count = self.count(tokens)
        len_A = len(self.A(tokens))
        alpha = 1.0

        if len_A > 0:
            # assert token_count > 0 , tokens
            alpha = self._beta * len_A / token_count
        return alpha

    def denom(self, tokens):
        """
        Normalization factor for a k-gram with 0 < k < n.
        tokens -- the k-gram tuple.
        """
        # assert isinstance(tokens, tuple), tokens
        denom = None
        if tokens in self._denom:
            denom = self._denom[tokens]
        else:
            denom = self.compute_denom(tokens)
            self._denom[tokens] = denom

        return denom

    def compute_denom(self, tokens):
        """
        Compute the normalization factor
        for a k-gram with 0 < k < n.
        tokens -- the k-gram tuple.
        """
        # assert isinstance(tokens, tuple), tokens
        A_set = self.A(tokens)
        sum_prob = 0.0
        for x in A_set:
            prob_x = self.cond_prob(x, tokens[1:])
            sum_prob += prob_x

        denom = 1.0 - sum_prob
        return denom

    def discount_count(self, tokens):
        return self.count(tokens) - self._beta

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        if not prev_tokens:
            prev_tokens = tuple()
        else:
            prev_tokens = tuple(prev_tokens)

        cond_prob = 0.0
        prev_count = float(self.count(prev_tokens))
        tokens = prev_tokens + (token,)
        tokens_count = self.count(tokens)

        if len(prev_tokens) == 0:  # Unigram
            if self._addone:
                tokens_count += 1.0
                prev_count += len(self._vocab)
            cond_prob = tokens_count / prev_count

        else:
            A_prev = self.A(prev_tokens)
            if token in A_prev:
                tokens_count -= self._beta  # Discount
                cond_prob = tokens_count / prev_count
            else:
                denom = self.denom(prev_tokens)
                if denom > 0:
                    alpha = self.alpha(prev_tokens)
                    prob = self.cond_prob(token, prev_tokens[1:])
                    cond_prob = alpha * prob / denom

        return cond_prob

    def estimate_beta(self, held_out):
        betas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

        perplexities = {}
        for beta in betas:
            self._beta = beta
            perp = self.perplexity(held_out)
            perplexities[beta] = perp
        best_beta = min(perplexities.items(), key=operator.itemgetter(1))[0]
        return best_beta
