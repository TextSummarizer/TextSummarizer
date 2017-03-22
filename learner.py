# from gensim.models import Word2Vec
import data as d

"""
https://codesachin.wordpress.com/2015/10/09/generating-a-word2vec-model-from-a-block-of-text-using-gensim-python/
https://radimrehurek.com/gensim/models/word2vec.html
https://rare-technologies.com/word2vec-tutorial/
http://textminingonline.com/getting-started-with-word2vec-and-glove-in-python
"""


sentences = d.get_data("file.xml")
sentences = d.remove_punctuation(sentences)
sentences = d.remove_doc(sentences)
d.print_data(sentences)
"""model = Word2Vec(iter=1)
model.build_vocab(sentences)
model.train(sentences)
vocab = list(model.vocab.keys())
print vocab
"""
