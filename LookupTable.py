import gensim


class LookupTable:
    def __init__(self, model_path):
        self.model = gensim.models.Word2Vec.load_word2vec_format(model_path, binary=True)

    def get(self, word):
        return self.model[word]
