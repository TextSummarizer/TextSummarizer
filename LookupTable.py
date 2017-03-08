import gensim


class LookupTable:
    def __init__(self, model_path):
        import os
        self.model = gensim.models.Word2Vec.load_word2vec_format(os.path.abspath(model_path), binary=True)

    def get(self, word):
        return self.model[word]
