# coding=utf-8
import lookup_table
import data as d
import numpy as np


class Summarizer:
    def __init__(self,
                 model_path=None,
                 stemming=False,
                 remove_stopwords=False,
                 tfidf_threshold=0.2,
                 regex=True,
                 redundancy_threshold=0.95):
        self.lookup_table = lookup_table.LookupTable(model_path)
        self.stemming = stemming
        self.remove_stopwords = remove_stopwords
        self.tfidf_threshold = tfidf_threshold
        self.regex = regex
        self.sentence_retriever = []  # populated in _preprocessing method
        self.redundancy_threshold = redundancy_threshold

    def set_tfidf_threshold(self, value):
        self.tfidf_threshold = value

    def set_redundancy_threshold(self, value):
        self.redundancy_threshold = value

    def summarize(self, text, summary_length, query_based_token):
        error_msg = self._check_params(self.redundancy_threshold, self.tfidf_threshold, summary_length)
        if not error_msg == "":
            return "==error==\n" + error_msg
        else:
            sentences = self._preprocessing(text, self.regex)
            centroid = self._gen_centroid_tfidf(sentences) \
                if not query_based_token \
                else self._gen_centroid_query_based(query_based_token)
            sentences_dict = self._sentence_vectorizer(sentences)
            summary = self._sentence_selection(centroid, sentences_dict, summary_length)
            return summary

    def _preprocessing(self, input_path, regex):
        # Get splitted sentences
        data = d.get_data(input_path)

        # Add points at the end of the sentence
        data = d.add_points(data)

        # Store the sentence before process them. We need them to build final summary
        self.sentence_retriever = data

        # Remove punctuation
        if regex:
            data = d.remove_punctuation_regex(data)
        else:
            data = d.remove_punctuation_nltk(data)

        # Gets the stem of every word if requested
        if self.stemming:
            data = d.stemming(data)

        # Remove stopwords if requested
        if self.remove_stopwords:
            data = d.remove_stopwords(data)

        return data

    def _gen_centroid_tfidf(self, sentences):
        from sklearn.feature_extraction.text import TfidfVectorizer
        import numpy as np

        # Get relevant terms
        tf = TfidfVectorizer()
        tfidf = tf.fit_transform(sentences).toarray().sum(0)
        tfidf = np.divide(tfidf, tfidf.max())
        words = tf.get_feature_names()

        relevant_terms = []
        for i in range(len(tfidf)):
            if tfidf[i] >= self.tfidf_threshold and not self.lookup_table.unseen(words[i]):
                relevant_terms.append(words[i])

        # Generate pseudo-doc
        res = [self.lookup_table.vec(term) for term in relevant_terms]
        return sum(res) / len(res)

    def _gen_centroid_query_based(self, query_based_token):
        res = [self.lookup_table.vec(term) for term in query_based_token]
        return sum(res) / len(res)

    def _sentence_vectorizer(self, sentences):
        dic = {}
        for i in range(len(sentences)):

            # Generate an array of zeros
            sum_vec = np.zeros(self.lookup_table.model.layer1_size)
            sentence = [word for word in sentences[i].split(" ") if not self.lookup_table.unseen(word)]

            # Sums all the word's vec to create the sentence vec if sentence is not empty
            # When can sentence be empty? When is composed from all unseen words
            if sentence:
                for word in sentence:
                    word_vec = self.lookup_table.vec(word)
                    sum_vec = np.add(sum_vec, word_vec)
                dic[i] = sum_vec / len(sentence)
        return dic

    def _sentence_selection(self, centroid, sentences_dict, summary_length):
        from scipy.spatial.distance import cosine
        import math

        # Generate ranked record (sentence_id - vector - sim_with_centroid)
        record = []
        for sentence_id in sentences_dict:
            vector = sentences_dict[sentence_id]
            sentence_length = len(self.sentence_retriever[sentence_id])
            centroid_similarity = (1 - cosine(centroid, vector))
            num = math.pow(centroid_similarity, 2)
            den = math.log(sentence_length)
            similarity = num / den
            record.append((sentence_id, vector, similarity))

        rank = list(reversed(sorted(record, key=lambda tup: tup[2])))

        # Get first k sentences until the limit (words%) is reached and avoiding redundancies
        sentence_ids = []
        summary_char_num = 0
        stop = False
        i = 0

        # Switch summarization mode: percentage VS number of sentences
        text_length = sum([len(x) for x in self.sentence_retriever])

        if summary_length <= 1:
            limit = int(text_length * summary_length)

            while not stop and i < len(rank):
                sentence_id = rank[i][0]
                new_vector = sentences_dict[sentence_id]
                sent_char_num = len(self.sentence_retriever[sentence_id])
                redundancy = [sentences_dict[k] for k in sentence_ids
                              if (1 - cosine(new_vector, sentences_dict[k]) > self.redundancy_threshold)]

                if not redundancy:
                    summary_char_num += sent_char_num
                    sentence_ids.append(sentence_id)
                i += 1

                if summary_char_num > limit:
                    stop = True
        else:
            sentences_number = summary_length
            sentence_ids = rank[:sentences_number]
            sentence_ids = map(lambda t: t[0], sentence_ids)

        sentence_ids = sorted(sentence_ids)
        result_list = map(lambda sent_id: self.sentence_retriever[sent_id], sentence_ids)

        # Format output
        summary = " ".join(result_list)
        # return summary[:char_limit]
        return summary

    @staticmethod
    def _check_params(redundancy, tfidf, summary_length):
        error_msg = ""

        try:
            assert 0 <= redundancy <= 1
        except AssertionError:
            error_msg += "ERRORE: la soglia sulla ridondanza inserita non è valida\n"

        try:
            assert 0 <= tfidf <= 1
        except AssertionError:
            error_msg += "ERRORE: la soglia sul tfidf inserita non è valida\n"

        try:
            assert  0 <= summary_length
        except AssertionError:
            error_msg += "ERRORE: l'indicazione sulla lunghezza del riassunto non è corretta\n"

        return error_msg
