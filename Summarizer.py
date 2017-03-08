import LookupTable


class Summarizer:
    def __init__(self, model_path, stemming, remove_stopwords, tfidf_threshold, coverage, redundancy_threshold):
        self.lookup_table = LookupTable(model_path)
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

    def _gen_centroid(self):
        pass

    def _phrase_vectorizer(self):
        pass

    def _phrase_selection(self):
        pass





