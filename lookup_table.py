import gensim
import numpy as np


class LookupTable:
    def __init__(self, model_path):
        import os
        #self.model = gensim.models.Word2Vec.load_word2vec_format(os.path.abspath(model_path), binary=True)
        self.model = gensim.models.Word2Vec.load(os.path.abspath(model_path))

    def vec(self, word):
        try:
            return self.model[word]
        except KeyError:
            return np.array([0])
