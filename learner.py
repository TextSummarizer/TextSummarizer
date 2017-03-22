#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gensim.models import Word2Vec
import data as d

sentences = d.get_data("file.xml")
sentences = d.remove_punctuation(sentences)
sentences = d.remove_doc(sentences)
sentences = [string.split(" ") for string in sentences]
model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
model.save("our_model")
model = Word2Vec.load("our_model")
print model.wv['è']
