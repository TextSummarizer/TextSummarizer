import lookup_table
import data as d
import numpy


class Summarizer:
    def __init__(self,
                 model_path=None,
                 stemming=False,
                 remove_stopwords=True,
                 tfidf_threshold=0.3,
                 summary_length=0.5,
                 redundancy_threshold=0.95):

        self.lookup_table = lookup_table.LookupTable(model_path)
        self.stemming = stemming
        self.remove_stopwords = remove_stopwords
        self.tfidf_threshold = tfidf_threshold
        self.sentence_retriever = []  # populated in _preprocessing method
        self.summary_length = summary_length
        self.redundancy_threshold = redundancy_threshold

    def summarize(self, input_path):
        sentences = self._preprocessing(input_path)

        centroid = self._gen_centroid(sentences)
        sentences_dict = self._sentence_vectorizer(sentences)
        summary = self._sentence_selection(centroid, sentences_dict)
        return summary

    def export(self, output_path):
        pass

    def _preprocessing(self, input_path):
        # Get splitted sentences
        data = d.get_data(input_path)

        # Add points at the end of the sentence
        data = d.add_points(data)

        # Store the sentence before process them. We need them to build final summary
        self.sentence_retriever = data

        # Remove punctuation
        data = d.remove_punctuation(data)

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
            sum_vec = numpy.zeros(self.lookup_table.model.layer1_size)
            sentence = [word for word in sentences[i].split(" ") if not self.lookup_table.unseen(word)]

            # Sums all the word's vec to create the sentence vec
            for word in sentence:
                word_vec = self.lookup_table.vec(word)
                sum_vec = numpy.add(sum_vec, word_vec)
            dic[i] = sum_vec / len(sentence)
        return dic

    def _sentence_selection(self, centroid, sentences_dict):
        from scipy.spatial.distance import cosine as cos_sim

        # Generate ranked record (sentence_id - vector - sim_with_centroid)
        record = []
        for sentence_id in sentences_dict:
            vector = sentences_dict[sentence_id]
            similarity = 1 - cos_sim(centroid, vector)
            record.append((sentence_id, vector, similarity))

        rank = list(reversed(sorted(record, key=lambda tup: tup[2])))

        # Get first k sentences until the limit (words%) is reached and avoiding redundancies
        word_count = sum([len(sentence.split(" ")) for sentence in self.sentence_retriever])
        word_limit = word_count * self.summary_length

        sentence_ids = []
        summary_word_num = 0
        stop = False
        i = 0

        while not stop and i < len(self.sentence_retriever):
            new_vector = sentences_dict[i]
            sent_word_num = len(self.sentence_retriever[i].split(" "))

            redundancy = [sentences_dict[k] for k in sentence_ids
                          if (1 - cos_sim(new_vector, sentences_dict[k]) > self.redundancy_threshold)]

            if not redundancy and i != 0:
                summary_word_num += sent_word_num
                sentence_id = rank[i][0]
                sentence_ids.append(sentence_id)
            i += 1

            if (summary_word_num + sent_word_num) > word_limit:
                stop = True

        sentence_ids = sorted(sentence_ids)
        result_list = map(lambda sent_id: self.sentence_retriever[sent_id], sentence_ids)

        # Format output
        return " ".join(result_list)
