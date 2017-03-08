import LookupTable


class Summarizer:
  def __init__(self, model_path=None, stemming=False, remove_stopwords=False,
               tfidf_threshold=0.5, coverage=0.5, redundancy_threshold=0.5):
    self.lookup_table = LookupTable.LookupTable(model_path)
    self.stemming = stemming
    self.remove_stopwords = remove_stopwords
    self.tfidf_threshold = tfidf_threshold
    self.coverage = coverage
    self.redundancy_threshold = redundancy_threshold

  def summarize(self, text_path):
    pass

  def export(self, output_path):
    pass

  def _preprocessing(self):
    pass

  def _gen_centroid(self, sentences):
    from sklearn.feature_extraction.text import TfidfVectorizer

    # Get relevant terms
    tf = TfidfVectorizer()
    tfidf = tf.fit_transform(sentences).toarray().sum(0)
    words = tf.get_feature_names()

    relevant_terms = []
    for i in range(len(tfidf)):
      if tfidf[i] >= self.tfidf_threshold:
        relevant_terms.append(words[i])

    # Generate pseudo-doc
    res = [self.lookup_table.get(term) for term in relevant_terms]
    return sum(res)

  def _phrase_vectorizer(self):
    pass

  def _phrase_selection(self):
    pass
