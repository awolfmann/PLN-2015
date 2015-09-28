from collections import Counter

class BaselineTagger:

    def __init__(self, tagged_sents):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        """
        tagged_text = [item for sent in tagged_sents for item in sent]
        self.bow = set([item[0] for item in tagged_text])

        self.bow_tagged = {}
        for word in self.bow:
            tagg_list = [item[1] for item in tagged_text if item[0] == word]
            tagg_count = Counter(tagg_list)
            top_tagg = tagg_count.most_common(1)[0][0]
            self.bow_tagged[word] = top_tagg
        print self.bow_tagged
   

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        return [self.tag_word(w) for w in sent]

    def tag_word(self, w):
        """Tag a word.

        w -- the word.
        """
        tag = None
        if not self.unknown(w):
            tag =  self.bow_tagged[w]
        else:
            tag = "UNK"
        return tag

    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
        return w not in self.bow 
