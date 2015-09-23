# https://docs.python.org/3/library/collections.html
from collections import defaultdict
import math
import random
from sets import Set
import operator


class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)
        self.len_v = 0
        words = []
        for sent in sents:
            init_markers = ['<s>' for _ in range(n - 1)]
            final_marker = ['</s>']
            sent_marked =  init_markers + sent + final_marker
            for i in range(len(sent_marked) - n + 1):
                ngram = tuple(sent_marked[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1
            words += sent 
        vocab = Set(words)
        vocab.add('</s>')
        self.len_v = len(vocab)

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
        prev_count  = self.counts[tuple(prev_tokens)]
        cond_prob = 0.0
        if  prev_count > 0:
            cond_prob = float(self.counts[tuple(tokens)]) / prev_count
        
        return cond_prob  
 
    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.
 
        tokens -- the n-gram or (n-1)-gram tuple.
        """
        return self.counts[tokens]

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.
 
        sent -- the sentence as a list of tokens.
        """
        n = self.n
        init_markers = ['<s>' for _ in range(n - 1)]
        final_marker = ['</s>']
        sent_marked =  init_markers + sent + final_marker
        sent_prob = 1.0
        
        for i in range(n - 1, len(sent_marked)):
            sent_prob *= self.cond_prob(sent_marked[i], sent_marked[i-n+1:i])
        return sent_prob
    
    def sent_log_prob(self, sent):
        """Log-probability of a sentence.
 
        sent -- the sentence as a list of tokens.
        """
        log2 = lambda x: math.log(x, 2)
        n = self.n
        init_markers = ['<s>' for _ in range(n - 1)]
        final_marker = ['</s>']
        sent_marked =  init_markers + sent + final_marker
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
            M += len(sent) + 1 # counting </s>
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
        perplexity = math.pow(2, cross_entropy)
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
        
        for ngram in model.counts.iterkeys():
            if len(ngram) == model.n:
                prev_tokens = ngram[:-1]
                token = ngram[-1]
                self.probs[prev_tokens][token] = model.cond_prob(token, list(prev_tokens))
            
        for key, value in self.probs.iteritems():

            self.sorted_probs[key] = sorted(value.iteritems(), key=lambda x: (-x[1], x[0]))

        self.sorted_probs = dict(self.sorted_probs)

    def generate_sent(self):
        """Randomly generate a sentence."""
        sent = []
        prev_tokens = ['<s>' for _ in range(self.model.n - 1)]
        token = self.generate_token(prev_tokens)
        # sent = prev_tokens + [token]
        sent = [token]
        while token != "</s>":
            prev_tokens = (prev_tokens + [token]) [1:] 
            token = self.generate_token(prev_tokens)
            sent.append(token)

        # ignore the "</s>"
        return sent[:-1]


    def generate_token(self, prev_tokens=None):
        """
        Randomly generate a token, given prev_tokens.
 
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.model.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1
        val = random.random()
        generated_token = None
        token_prob_list = self.sorted_probs[tuple(prev_tokens)]
        acum_prob = 0.0
        # while val > acum_prob: agregar indice
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
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]
        return float(self.counts[tuple(tokens)] + 1) / (self.counts[tuple(prev_tokens)] + self.len_v)
 
    def V(self):
        """Size of the vocabulary.
        """
        return self.len_v


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
        self.n = n
        self.counts = counts = defaultdict(int)
        self.len_v = 0
        self.addone = addone

        if gamma is not None:
            self.gamma = gamma
        else:
            held_out = sents[int(0.9*len(sents)):]
            sents = sents[:int(0.9*len(sents))]
            self.gamma = self.estimate_gamma(held_out)

        words = []
        for sent in sents:
            init_markers = ['<s>' for _ in range(n - 1)]
            final_marker = ['</s>']
            sent_marked =  init_markers + sent + final_marker
            counts[('<s>',)] += 1
            for i in range(len(sent_marked) - n + 1):
                ngram = tuple(sent_marked[i: i + n])
                counts[ngram] += 1
                for j in range(1, n + 1):
                    counts[ngram[j:]] += 1
            counts[('<s>',)] += 1 # The first unigram is ignored in the recursion
            words += sent_marked 
        vocab = Set(words)
        vocab.add('</s>')
        self.len_v = len(vocab)
        self.len_w = len(words)

    def fill_count(self, counts, sents):
        words = []
        for sent in sents:
            init_markers = ['<s>' for _ in range(n - 1)]
            final_marker = ['</s>']
            sent_marked =  init_markers + sent + final_marker
            for i in range(len(sent_marked) - n + 1):
                ngram = tuple(sent_marked[i: i + n])
                counts[ngram] += 1
                for j in range(1, n):
                    counts[ngram[:-j]] += 1
            words += sent 
        vocab = Set(words)
        vocab.add('</s>')

        return (count, len(vocab))


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
        sum_lamdas = 0.0 
        cond_prob = 0.0

        for i in range(n):
            lamda = self.lamda(i+1, sum_lamdas, prev_tokens[i:])
            sum_lamdas += lamda
            prev_count  = self.counts[tuple(prev_tokens[i:])]
            tokens_count = float(self.counts[tuple(tokens)]) 
            
            if len(prev_tokens[i:]) == 0 and self.addone: # Unigram
                tokens_count += 1.0
                prev_count += self.len_v 
            if lamda > 0.0 and prev_count > 0:
                c = tokens_count / prev_count
                cond_prob += lamda * c

        return cond_prob

    def lamda(self, i, sum_lamdas, tokens):
        """calculate the ith lambda"""
        lamda = 0.0
        if i < self.n:
            c = self.counts[tuple(tokens)] / float(self.counts[tuple(tokens)] + self.gamma) 
            lamda = (1.0 - sum_lamdas) * c 
        else:
            lamda = 1.0 - sum_lamdas

        return lamda

    def estimate_gamma(self, held_out):
        # perplexity como metodo
        # from languagemodeling.scripts.eval import Eval
        gammas = [math.pow(10, x) for x in range(5)]
        train_sents = held_out[:int(0.9*len(held_out))]
        eval_sents = held_out[int(0.9*len(held_out)):]

        perplexities = {}
        for gamma in gammas:
            model = InterpolatedNGram(self.n, train_sents, gamma)
            evalulator = Eval(model)
            perp = evalulator.perplexity(eval_sents)
            perplexities[gamma] = perp

        best_gamma = max(perplexities.iteritems(), key=operator.itemgetter(1))[0]
        
        return best_gamma
        # dividir el train en 0.9 y 0.1, si viene dado no lo dividis
        # con el 0.9 calculas los counts, probas 
        # beta= 0.5, 0.1, 0.9
        # gamma = 0, 50, 100, si sigue subiendo la perplexity, seguis aumentando
        # con eso tenes modelo definido y calculas perplexity sobre el 0.1

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
        self.n = n
        self.counts = counts = defaultdict(int)
        self.len_v = 0
        self.addone = addone
        if beta is not None:
            self.beta = beta
        else:
            held_out = sents[int(0.9*len(sents)):]
            sents = sents[:int(0.9*len(sents))]
            self.beta = self.estimate_beta(held_out)

        self._alpha = {}
        self._denom = {}
        self._A = {}
        words = []
        for sent in sents:
            init_markers = ['<s>' for _ in range(n - 1)]
            final_marker = ['</s>']
            sent_marked =  init_markers + sent + final_marker
            
            for i in range(len(sent_marked) - n + 1):
                ngram = tuple(sent_marked[i: i + n])
                counts[ngram] += 1
                for j in range(1, n + 1):
                    counts[ngram[j:]] += 1
            counts[('<s>',)] += 1 # The first unigram is ignored in the recursion
            words += sent 
        vocab = Set(words)
        vocab.add('</s>')
        self.vocab = vocab

    def A(self, tokens):
        """Set of words with counts > 0 for a k-gram with 0 < k < n.
 
        tokens -- the k-gram tuple.
        """
        assert len(tokens) < self.n
        try:
            A = self._A[tuple(tokens)]
        except KeyError:
            A = self.compute_A(tokens)
            self._A[tuple(tokens)] = A
        return A

    def compute_A(self, tokens):
        A = { word for word in self.vocab if self.counts[tuple(tokens) + (word,)] > 0 }
        return A

    def alpha(self, tokens):
        """Missing probability mass for a k-gram with 0 < k < n.
 
        tokens -- the k-gram tuple.
        """
        # _alpha.get(tokens, 1.0)
        try:
            alpha = self._alpha[tuple(tokens)]
        except KeyError:
            alpha = self.compute_alpha(tokens)
            self._alpha[tuple(tokens)] = alpha

        return alpha
    
    def compute_alpha(self, tokens):
        """Missing probability mass for a k-gram with 0 < k < n.
 
        tokens -- the k-gram tuple.
        """
        token_count = self.counts[tuple(tokens)]
        alpha = 1.0
        if token_count > 0:
            alpha = self.beta * len(self.A(tokens)) / token_count
        return alpha
 
    def denom(self, tokens):
        """Normalization factor for a k-gram with 0 < k < n.
 
        tokens -- the k-gram tuple.
        """ 
        try:
            denom = self._denom[tuple(tokens)]
        except KeyError:
            denom = self.compute_denom(tokens)
            self._denom[tuple(tokens)] = denom

        return denom

    def compute_denom(self, tokens):
        """Normalization factor for a k-gram with 0 < k < n.
 
        tokens -- the k-gram tuple.
        """ 
        A_set = self.A(tokens)
        sum_prob = 0.0
        for x in A_set:
            prob_x = self.cond_prob(x, tokens[1:])
            sum_prob += prob_x

        denom = 1.0 - sum_prob
        return denom 

    def discount_count(self, tokens):
        return self.counts[tuple(tokens)] - self.beta

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
 
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = []

        A_prev = self.A(prev_tokens)
        cond_prob = 0.0
        if token in A_prev:
            tokens = prev_tokens + [token]
            prev_count  = float(self.counts[tuple(prev_tokens)])
            tokens_count = self.discount_count(tokens)
            
            if len(prev_tokens) == 0:
                tokens_count = self.counts[tuple(tokens)]
                if self.addone: # Unigram
                    tokens_count += 1.0 
                    prev_count += len(self.vocab)
            if prev_count > 0:
                cond_prob = tokens_count /  prev_count 
        else:
            denom = self.denom(prev_tokens)
            if denom > 0.0:
                cond_prob = self.alpha(prev_tokens) * self.cond_prob(token, prev_tokens[1:]) / denom

        return cond_prob

    def estimate_beta(self, held_out):
        from languagemodeling.scripts.eval import Eval
        betas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        train_sents = held_out[:int(0.9*len(held_out))]
        eval_sents = held_out[int(0.9*len(held_out)):]

        perplexities = {}
        for beta in betas:
            model = BackOffNGram(self.n, train_sents, beta)
            evalulator = Eval(model)
            perp = evalulator.perplexity(eval_sents)
            perplexities[beta] = perp

        best_beta = max(perplexities.iteritems(), key=operator.itemgetter(1))[0]
        
        return best_beta
# Interpolado, cuando sea con unigrama, usar addone, 
# cuando viene el parametro addone en true, sino, en false no se usa
# Gamma depende del corpus, mientras mas grande el gamma, 
# mas chico el lambda mientras mas agrando el gamma, menos confio 
# en los modelos mas grandes del train