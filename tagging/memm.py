from featureforge.vectorizer import Vectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

from tagging.features import (History, word_lower, word_istitle, word_isupper,
                              word_isdigit, word_len, NPrevTags, PrevWord, 
                              word_prefix, word_sufix)

class MEMM(object):

    def __init__(self, n, tagged_sents, clf=LogisticRegression):
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        """
        self.n = n
        tagged_text = [item for sent in tagged_sents for item in sent]
        self.bow = set([item[0] for item in tagged_text])
        self.features= [word_lower, word_istitle, word_isupper, word_isdigit]
        
        prev_word_features = []
        for feature in self.features:
            prev_word_features.append(PrevWord(feature))

        self.features += prev_word_features

        prev_tags_features = []
        for i in range (1,n):
            prev_tags_features.append(NPrevTags(i))
        self.features += prev_tags_features
        self.pipeline = Pipeline([('vect', Vectorizer(self.features)),
                                ('clf', clf()),
                                ])
        self.pipeline.fit(self.sents_histories(tagged_sents), 
                        self.sents_tags(tagged_sents) )

    def sents_histories(self, tagged_sents):
        """
        Iterator over the histories of a corpus.
 
        tagged_sents -- the corpus (a list of sentences)
        """
        histories = []
        for tagged_sent in filter(lambda x: x, tagged_sents):
            histories += self.sent_histories(tagged_sent)
            # yield self.sent_histories(tagged_sent)
        return histories
 		
    def sent_histories(self, tagged_sent):
        """
        Iterator over the histories of a tagged sentence.
 
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        sent, tags = zip(*tagged_sent)
        histories = []
        prev_tags = ['<s>'] * (self.n - 1)
        prev_tags = tuple(prev_tags)
        for i, (w,t) in enumerate(tagged_sent):
            h = History(list(sent), prev_tags, i)
            prev_tags = (prev_tags + (t,))[1:]
            histories += [h]

        return histories

    def sents_tags(self, tagged_sents):
        """
        Iterator over the tags of a corpus.
 
        tagged_sents -- the corpus (a list of sentences)
        """
        tags = []
        for tagged_sent in tagged_sents:
            tags += self.sent_tags(tagged_sent)

        return tags

    def sent_tags(self, tagged_sent):
        """
        Iterator over the tags of a tagged sentence.
 
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        tags = []
        for _, tag in tagged_sent:
            tags += [tag]

        return tags

    def tag(self, sent):
        """Tag a sentence.
        sent -- the sentence.
        """
        tags = []
        prev_tags = ['<s>'] * (self.n - 1)
        prev_tags = tuple(prev_tags)
        for i, _ in enumerate(sent):
            h = History(sent, prev_tags, i)
            tag = self.tag_history(h)
            tags += [tag]
            prev_tags = (prev_tags + (tag,))[1:]
        
        return tags
    
    def tag_history(self, h):
        """Tag a history.
        h -- the history.
        """
        tag = self.pipeline.predict([h])[0]
        return tag
    
    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
        return w not in self.bow
