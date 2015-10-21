from collections import Counter
from itertools import groupby

class BaselineTagger:

    def __init__(self, tagged_sents):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        """
        tagged_text = [item for sent in filter(lambda x: x, tagged_sents) for item in sent]
        self.bow = set([item[0] for item in tagged_text])
        tags = [item[1] for item in tagged_text]
        self.most_common_tag = Counter(tags).most_common(1)[0][0]
        self.bow_tagged = {}

        for word, tag_group in groupby(tagged_text, lambda x: x[0]):
            tag_list = [item[1] for item in tag_group]
            top_tag = max(set(tag_list), key=tag_list.count)
            self.bow_tagged[word] = top_tag

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
            tag = self.most_common_tag
        return tag

    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
        return w not in self.bow 
