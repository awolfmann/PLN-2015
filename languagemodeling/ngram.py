# https://docs.python.org/3/library/collections.html
from collections import defaultdict
import math
import random
from sets import Set


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
        return float(self.counts[tuple(tokens)]) / self.counts[tuple(prev_tokens)]
 
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
        
        for i in range(n, len(sent_marked)):
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
        sent_log_prob = 1.0
        
        for i in range(n, len(sent_marked)):
            sent_log_prob *= log2(self.cond_prob(sent_marked[i], sent_marked[i-n+1:i]))

        return sent_log_prob


class NGramGenerator(object):
 
    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self.model = model
        self.sorted_probs = {}
        self.probs = {}

        # for ngram in self.model.counts:
            
        # cargar aca el probs y el sorted probs

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
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1
        val = random.random()
        sorted_probs[tuple(prev_tokens)]
        # p(x|el) = 0.5 si x = perro
        #           0.3 si x = gato 
        # generar random, si  cae entre 0 y 0.5 es perro, 0.5 y 0.8 es gato
        # usar sorted probs ordenado de mayor a menor para q termine antes  

class AddOneNGram(NGram):
    # def __init__(self, n, sents, len_v):
    #     super(AddOneNGram, self).__init__(n, sents)
    #     self.len_v = len_v 
    # def __init__(self, n, sents):
    #     """
    #     n -- order of the model.
    #     sents -- list of sentences, each one being a list of tokens.
    #     len_v -- size of the vocabulary.
    #     """
    #     assert n > 0
    #     self.n = n
    #     self.counts = counts = defaultdict(int)
    #     self.len_v = len_v

    #     for sent in sents:
    #         init_markers = ['<s>' for _ in range(n - 1)]
    #         final_marker = ['</s>']
    #         sent_marked =  init_markers + sent + final_marker
    #         for i in range(len(sent_marked) - n + 1):
    #             ngram = tuple(sent_marked[i: i + n])
    #             counts[ngram] += 1
    #             counts[ngram[:-1]] += 1 

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


# Interpolado, cuando sea con unigrama, usar addone, 
# cuando viene el parametro addone en true, sino, en false no se usa
# Gamma depende del corpus, mientras mas grande el gamma, mas chico el lambda
# mientras mas agrando el gamma, menos confio en los modelos mas grandes del train

# para los ultimos ejercicios usar un unico diccionario, usar un unico dict de counts para todos los k gramas
# nltk tiene un modelo de back off, cada uno  de los metodos debe ir a un dict precalculado en el init, 3 A, alpha y denom
# para interpolado si el lambda te da 0 no calcular la prob y no dividir por 0