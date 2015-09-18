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
<<<<<<< HEAD
                # word = sent_marked[i]
                # counts[word] +=1
=======
>>>>>>> 291881450e6175cd6b59ab8524605c2a1dec1e71
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
        self.gamma = gamma
        self.addone = addone

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
           
        lamdas = [] # Sirve tener una lista de los lamdas o con la suma alcanza?
        # Ver como iterar con los tokens
        # Falta considerar addone
        # Held out data?
        cond_prob = 0.0
        for i in  range(1, n+1):
            lamda = self.lamda(i, lamdas, tokens)
            lamdas.append(lamda)
            if lamda > 0.0:
                c = float(self.counts[tuple(tokens)]) / self.counts[tuple(prev_tokens)]
                cond_prob += lamda * c

    def lamda(self, i, lamdas, tokens):
        lamda = 0.0
        if i < self.n:
            c = self.counts[tuple(tokens)] / float(self.counts[tuple(tokens)] + self.gamma) 
            lamda = (1.0 - sum(lamdas)) * c 
        else:
            lamda = 1.0 - sum(lamdas)

        return lamda


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
        self.beta = beta
        self.addone = addone

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
        self.len_v = len(vocab)


    def A(self, tokens):
        """Set of words with counts > 0 for a k-gram with 0 < k < n.
 
        tokens -- the k-gram tuple.
        """
 
    def alpha(self, tokens):
        """Missing probability mass for a k-gram with 0 < k < n.
 
        tokens -- the k-gram tuple.
        """
 
    def denom(self, tokens):
        """Normalization factor for a k-gram with 0 < k < n.
 
        tokens -- the k-gram tuple.
        """
# Interpolado, cuando sea con unigrama, usar addone, 
# cuando viene el parametro addone en true, sino, en false no se usa
# Gamma depende del corpus, mientras mas grande el gamma, 
# mas chico el lambda mientras mas agrando el gamma, menos confio 
# en los modelos mas grandes del train

# para los ultimos ejercicios usar un unico diccionario, usar un 
# unico dict de counts para todos los k gramas nltk tiene 
# un modelo de back off, cada uno  de los metodos debe ir a un dict precalculado en el init, 3 A, alpha y denom

# para interpolado si el lambda te da 0 no calcular la prob y no dividir por 0