import lookup_table
import data as d
import numpy as np


class Summarizer:
    def __init__(self,
                 model_path=None,
                 stemming=False,
                 remove_stopwords=False,
                 regex=True,
                 tfidf_threshold=0.3,
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

    def summarize(self, input_path, summary_length):
        sentences = self._preprocessing(input_path, self.regex)
        centroid = self._gen_centroid(sentences)
        sentences_dict = self._sentence_vectorizer(sentences)
        summary = self._sentence_selection(centroid, sentences_dict, summary_length)
        return summary

    def export(self, output_path):
        pass

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

    def _gen_centroid(self, sentences):
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
        from scipy.spatial.distance import cosine as cos_sim

        # Generate ranked record (sentence_id - vector - sim_with_centroid)
        record = []
        for sentence_id in sentences_dict:
            vector = sentences_dict[sentence_id]
            similarity = 1 - cos_sim(centroid, vector)
            record.append((sentence_id, vector, similarity))

        rank = list(reversed(sorted(record, key=lambda tup: tup[2])))

        # Get first k sentences until the limit (words%) is reached and avoiding redundancies
        # word_count = sum([len(sentence.split(" ")) for sentence in self.sentence_retriever])
        # word_limit = word_count * summary_length
        char_limit = summary_length

        sentence_ids = []
        summary_char_num = 0
        stop = False
        i = 0

        while not stop and i < len(rank):
            sentence_id = rank[i][0]
            new_vector = sentences_dict[sentence_id]
            sent_char_num = len(self.sentence_retriever[sentence_id])

            redundancy = [sentences_dict[k] for k in sentence_ids
                          if (1 - cos_sim(new_vector, sentences_dict[k]) > self.redundancy_threshold)]

            if not redundancy:
                summary_char_num += sent_char_num
                sentence_ids.append(sentence_id)
            i += 1

            if summary_char_num > char_limit:
                stop = True

        sentence_ids = sorted(sentence_ids)
        result_list = map(lambda sent_id: self.sentence_retriever[sent_id], sentence_ids)

        # Format output
        return " ".join(result_list)
