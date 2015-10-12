class MEMM(object):

    def __init__(self, n, tagged_sents):
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        """
        # en el init de memm llamar a fit 
        self.n = n
        tagged_text = [item for sent in tagged_sents for item in sent]
        self.bow = set([item[0] for item in tagged_text])
 
    def sents_histories(self, tagged_sents):
        """
        Iterator over the histories of a corpus.
 
        tagged_sents -- the corpus (a list of sentences)
        """
        for tagged_sent in tagged_sents:
            yield self.sent_histories(tagged_sent)
 
    def sent_histories(self, tagged_sent):
        """
        Iterator over the histories of a tagged sentence.
 
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
 
    def sents_tags(self, tagged_sents):
        """
        Iterator over the tags of a corpus.
 
        tagged_sents -- the corpus (a list of sentences)
        """
        for tagged_sent in tagged_sents:
            yield self.sent_tags(tagged_sent)
    def sent_tags(self, tagged_sent):
        """
        Iterator over the tags of a tagged sentence.
 
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
 
    def tag(self, sent):
        """Tag a sentence.
        sent -- the sentence.
        """
        # beam inference 
    
    def tag_history(self, h):
        """Tag a history.
        h -- the history.
        """
        pipeline.predict(h)
    
    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
        return w not in self.bow