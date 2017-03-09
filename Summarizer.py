import LookupTable
import Data


class Summarizer:
    def __init__(self, model_path=None, stemming=False, remove_stopwords=False,
                 tfidf_threshold=0.5, coverage=0.5, redundancy_threshold=0.5):
        self.lookup_table = LookupTable.LookupTable(model_path)
        self.stemming = stemming
        self.remove_stopwords = remove_stopwords
        self.tfidf_threshold = tfidf_threshold
        self.sentence_retriever = []
        self.coverage = coverage
        self.redundancy_threshold = redundancy_threshold

    def summarize(self, text_path):
        pass

    def export(self, output_path):
        pass

    def _preprocessing(self, input_path):
        d = Data.Data()
        # Get splitted sentences
        data = d.get_data(input_path)

        # Add points at the end of the sentence
        data = d.add_points(data)

        # Gets the stem of every word if requested
        if self.stemming:
            data = d.stemming(data)

        # Remove stopwords if requested
        if self.remove_stopwords:
            data = d.remove_stopwords(data)

        return data

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
        res = [self.lookup_table.vec(term) for term in relevant_terms]
        return sum(res)

    def _sentence_vectorizer(self):
        pass

    def _sentence_selection(self, centroid, sentences_dict):
        from sklearn.metrics.pairwise import cosine_similarity

        # Generate ranked record (sentence_id - vector - sim_with_centroid)
        centroid = centroid.reshape(1, -1)  # avoid warning
        record = []
        for sentence_id in sentences_dict:
            vector = sentences_dict[sentence_id].reshape(1, -1)
            similarity = cosine_similarity(centroid, vector)
            record.append((sentence_id, vector, similarity[0, 0]))

        rank = list(reversed(sorted(record, key=lambda tup: tup[2])))

        # Get first k sentences until the limit (words%) is reached
        word_count = sum([len(sentence.split(" ")) for sentence in self.sentence_retriever])
        word_limit = word_count * self.coverage

        result_list = []
        summary_word_num = 0
        stop = False
        i = 0
        while not stop and i < len(self.sentence_retriever):
            sent_word_num = len(self.sentence_retriever[i].split(" "))
            if (summary_word_num + sent_word_num) <= word_limit:
                summary_word_num += sent_word_num
                sentence_id = rank[i][0]
                result_list.append(self.sentence_retriever[sentence_id])
                i += 1
            else:
                stop = True

        # Format output
        result = ""
        for sentence in result_list:
            result += sentence

        return result


s = Summarizer()
print s.preprocessing("testo.txt")
