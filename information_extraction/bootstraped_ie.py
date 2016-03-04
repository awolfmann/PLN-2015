from featureforge.vectorizer import Vectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

from features import (History, prev_features, post_features, middle_features, arg1_features, arg2_features)


class IE(object):

    def __init__(self, processed_sents, clf='LR'):
        """
        n -- order of the model.
        processed_sents -- list of sentences, each one being a list of tuples, 
        with the relations extracted on it
        clf -- classifier
        """
        # self.n = n
        # preprocessed_text = [item for sent in preprocessed_sents for item in sent]
        # self.bow = set([item[0] for item in preprocessed_text])
        prev_words, prev_tags, prev_entities = prev_features
        middle_words, middle_tags, middle_entities = middle_features
        post_words, post_tags, post_entities = post_features
        self.features = [prev_words, prev_tags, prev_entities,
                         middle_words, middle_tags, middle_entities,
                         post_words, post_tags, post_entities]


        classifier = None
        if clf == 'DT':
            classifier = DecisionTreeClassifier
        elif clf == 'LR':
            classifier = LogisticRegression
        # elif clf == 'SVC':
        #     classifier = LinearSVC

        self.pipeline = Pipeline([('vect', Vectorizer(self.features)),
                                 ('clf', classifier())]
                                 )
        self.pipeline.fit(self.sents_histories(processed_sents),
                          self.sents_tags(processed_sents))

    def sents_histories(self, processed_sents):
        """
        Iterator over the histories of a corpus.
        preprocessed_sents -- the corpus (a list of preprocessed sentences)
        """
        histories = []
        for processed_sent in filter(lambda x: x, processed_sents):
            histories += self.sent_histories(processed_sent)
        return histories

    def sent_histories(self, processed_sent):
        """
        Iterator over the histories of a tagged sentence.
        processed_sent -- the processed sent sentence (a list of tuples (word, tag, entity)).
        """
        sent, tags, entities = zip(*processed_sent)
        histories = []
        if len(set(entities)) > 3 :
        # NO sirve, si las 2 entidades son del mismo tipo 
        # Si hay mas de 3 entidades distintitas, puede haber relacion binaria 
        # VER QUE PASA CON STANFORD UNIVERSITY is located in california, son 2 entidades juntas..
        # Ver como reconocer la palabra clave, ya que no necesariamente es un verbo, usar arbol de parseo? 
        # Como hacer si hay mas de una relacion en la misma oracion?
            # rels = [i for i,x in enumerate(tags) if x == 'VERBO']
            # rel = processed_sent[rels] # VER SI SON MAS DE UNO
            entities = [i for i,x in enumerate(entities) if x == 'ENTIDAD']
            arg1_pos = entities[0]
            arg1 = processed_sent[arg1_pos] # VER SI SON MAS DE UNO
            arg2_pos = entities[1]
            arg2 = processed_sent[arg2_pos]
            prev = processed_sent[:arg1_pos]
            post = processed_sent[arg2_pos:]
            middle = processed_sent[arg1_pos:arg2_pos]
            h = History(sent, rel, prev, arg1, middle, arg2, post)

        return h

    def sents_relations(self, processed_sents):
        """
        Iterator over the tags of a corpus.
        processed_sents -- the corpus (a list of sentences)
        """
        relations = []
        for processed_sent in processed_sents:
            # relations += self.sent_relations(processed_sents)
            relations += processed_sent[1]
        return relations

    def sent_relations(self, processed_sent):
        """
        Iterator over the relations of a processed sentence.
        processed_sent -- the processed_sent sentence (a pair of list (sent, relations)).
        """

        return processed_sents[1]

    def process_sent(self, sent):
        """Extract relations from a sentence.
        sent -- the sentence.
        """
        relations = []
        prev_tags = ['<s>'] * (self.n - 1)
        prev_tags = tuple(prev_tags)
        for i, _ in enumerate(sent):
            h = History(sent, prev_tags, i)
            tag = self.tag_history(h)
            tags += [tag]
            prev_tags = (prev_tags + (tag,))[1:]

        return tags

    def process_history(self, h):
        """Tag a history.
        h -- the history.
        """
        relation = self.pipeline.predict([h])[0]
        return relation

    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
        return w not in self.bow
