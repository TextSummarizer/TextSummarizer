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
                 redundancy_threshold=0.95,
                 default_centroid_mode="tfidf",
                 num_topics_lda=4,
                 num_words_lda=5,
                 language="italian"):
        self.lookup_table = lookup_table.LookupTable(model_path)
        self.stemming = stemming
        self.remove_stopwords = remove_stopwords
        self.tfidf_threshold = tfidf_threshold
        self.regex = regex
        self.sentence_retriever = []  # populated in _preprocessing method
        self.redundancy_threshold = redundancy_threshold
        self.default_centroid_mode = default_centroid_mode
        self.num_topics_lda = num_topics_lda
        self.num_words_lda = num_words_lda
        self.language = language

    def set_tfidf_threshold(self, value):
        self.tfidf_threshold = value

    def set_redundancy_threshold(self, value):
        self.redundancy_threshold = value

    def summarize(self, text, summary_length, query_based_token):
        error_msg = self._check_params(self.redundancy_threshold, self.tfidf_threshold, summary_length)
        error_flag = False

        if error_msg != "":
            return "", error_msg, True

        if query_based_token:
            centroid_mode = CentroidMode.QUERY_BASED
        else:
            centroid_mode = self.default_centroid_mode

        # Sentences generation (with preprocessing) + centroid generation (based on centroid_mode choice)
        sentences = self._preprocessing(text, self.regex, centroid_mode)

        print "CENTROIDE MODE:", str(centroid_mode)

        if centroid_mode == CentroidMode.QUERY_BASED:
            centroid, error_msg = self._gen_centroid_query_based(query_based_token)
            if centroid is None:
                return "", error_msg, True
            elif error_msg is not "":
                error_flag = True

        elif centroid_mode == CentroidMode.TFIDF:
            centroid = self._gen_centroid_tfidf(sentences)

        elif centroid_mode == CentroidMode.LDA:
            sentences_split = [sentence.split(" ") for sentence in sentences]
            sentences_for_centroid = []
            for sentence in sentences_split:
                sentences_for_centroid.append(filter(lambda word: word != '', sentence))
            centroid = self._gen_centroid_lda(sentences_for_centroid, self.num_topics_lda, self.num_words_lda)

        else:
            error_msg += ErrorMessage.INVALID_CENTROID_MODE
            return "", error_msg, True

        # Sentence vectorization + sentence selection
        sentences_dict = self._sentence_vectorizer(sentences)
        summary = self._sentence_selection(centroid, sentences_dict, summary_length)

        return summary, error_msg, error_flag

    def _preprocessing(self, text, regex, centroid_mode):
        # import unidecode

        # text_utf = unicode(text, 'utf8')
        # text_ascii = unidecode.unidecode(text_utf)

        if centroid_mode == CentroidMode.LDA:
            self.remove_stopwords = True
            self.stemming = True

        # Get splitted sentences
        sentences = d.get_data(text, self.language)
        sentences_original = d.get_data(text, self.language)  # We need them in sentence retriever

        # Add points at the end of the sentence
        # sentences = d.add_points(sentences)
        # sentences_original = d.add_points(sentences_original)  # We need them in sentence retriever

        # Store the sentence before process them. We need them to build final summary
        self.sentence_retriever = sentences_original

        # Remove punctuation
        if regex:
            sentences = d.remove_punctuation_regex(sentences)
        else:
            sentences = d.remove_punctuation_nltk(sentences)

        # Gets the stem of every word if requested
        if self.stemming:
            sentences = d.stemming(sentences)

        # Remove stopwords if requested
        if self.remove_stopwords:
            sentences = d.remove_stopwords(sentences)

        # sent = sentences[1]
        # sentences_ascii = [unidecode.unidecode(sentence) for sentence in sentences]
        # prova = sentences_ascii[1]
        # print prova

        return sentences

    def _gen_centroid_lda(self, sentences, num_topics, num_words):
        from gensim import models, corpora

        # Find topic and probability distribution for each topic (with LDA)
        dictionary = corpora.Dictionary(sentences)  # Usage: remember (id -> term) mapping
        corpus = [dictionary.doc2bow(text) for text in sentences]  # build matrix (corpus is the matrix)
        lda_model = models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary)
        show_topics = lda_model.show_topics()

        # For each topic, I want to get only "num_words" term (the most relevant, based on probability distribution)
        # Selected token will be part of my "centroid_set"
        # Warning: I have to filter out relevant words that are not in w2v model
        centroid_set = []
        for topic in show_topics:
            token_probability_records = topic[1].split(" + ")
            i = 0
            topic_word_counter = 0
            stop = False

            while i < len(token_probability_records) and not stop:
                # String manipulation (probability distribution is in string format)
                next_record = token_probability_records[i]
                split_record = next_record.split("*")
                token = split_record[1].replace("\"", "")  # (split_record[0] is probability of the token)

                if token not in centroid_set:
                    if not self.lookup_table.unseen(token):
                        centroid_set.append(token)
                        topic_word_counter += 1
                        if topic_word_counter == num_words:
                            stop = True
                i += 1

        top_words_vectorized = map(lambda word: self.lookup_table.vec(word), centroid_set)
        return sum(top_words_vectorized) / len(top_words_vectorized)

    def _gen_centroid_tfidf(self, sentences):
        from sklearn.feature_extraction.text import TfidfVectorizer

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
        query_based_token = query_based_token.lower()
        seen_token = [token for token in query_based_token if not self.lookup_table.unseen(token)]
        unseen_token = [token for token in query_based_token if self.lookup_table.unseen(token)]

        if not seen_token:
            return None, ErrorMessage.generate_query_based_error()

        warning_msg = ""
        if unseen_token:
            warning_msg = ErrorMessage.generate_query_based_warning(unseen_token, seen_token)
        res = [self.lookup_table.vec(term) for term in seen_token]
        centroid = sum(res) / len(res)
        return centroid, warning_msg

    def _sentence_vectorizer(self, sentences):
        dic = {}
        for i in range(len(sentences)):

            # Generate an array of zeros
            sum_vec = np.zeros(self.lookup_table.model.vector_size)
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

        #summary_length = int(summary_length)

        # Generate ranked record (sentence_id - vector - sim_with_centroid)
        record = []
        for sentence_id in sentences_dict:
            vector = sentences_dict[sentence_id]
            similarity = (1 - cosine(centroid, vector))
            record.append((sentence_id, vector, similarity))

        rank = list(reversed(sorted(record, key=lambda tup: tup[2])))

        # Get first k sentences until the limit (words%) is reached and avoiding redundancies
        sentence_ids = []
        summary_char_num = 0
        stop = False
        i = 0

        # Switch summarization mode: percentage VS number of sentences
        text_length = sum([len(x) for x in self.sentence_retriever])

        if summary_length < 1:  # Base summary length on percentage
            #limit = int(text_length * summary_length)
            limit = int(text_length * float(summary_length))

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
        else:  # Base summary length on number of sentences
            sentences_number = int(summary_length)
            sentence_ids = rank[:sentences_number]
            sentence_ids = map(lambda t: t[0], sentence_ids)

        sentence_ids = sorted(sentence_ids)
        result_list = map(lambda sent_id: self.sentence_retriever[sent_id], sentence_ids)

        # Format output
        summary = " ".join(result_list)
        return summary

    @staticmethod
    def _check_params(redundancy, tfidf, summary_length):
        error_msg = ""

        try:
            assert 0 <= redundancy <= 1
        except AssertionError:
            error_msg += ErrorMessage.INVALID_REDUNDANCY

        try:
            assert 0 <= tfidf <= 1
        except AssertionError:
            error_msg += ErrorMessage.INVALID_TFIDF

        try:
            assert 0 <= summary_length
        except AssertionError:
            error_msg += ErrorMessage.INVALID_LENGTH

        return error_msg


class CentroidMode:
    def __init__(self):
        pass

    QUERY_BASED = "query_based"
    TFIDF = "tfidf"
    LDA = "lda"


class ErrorMessage:
    def __init__(self):
        pass

    INVALID_CENTROID_MODE = "Centroid_mode non è avvalorato correttamente. Valori accettati: (lda - tfidf - query_based)"
    INVALID_REDUNDANCY = "ERRORE: la soglia sulla ridondanza inserita non è valida\n"
    INVALID_TFIDF = "ERRORE: la soglia sul tfidf inserita non è valida\n"
    INVALID_LENGTH = "ERRORE: l'indicazione sulla lunghezza del riassunto non è corretta\n"

    @staticmethod
    def generate_query_based_warning(unseen_token, seen_token):
        return "Non è stato possibile utilizzare i termini: " + ", ".join(unseen_token) + "\n" + \
               "Il riassunto è stato comunque generato utilizzando i termini: " + ", ".join(seen_token)

    @staticmethod
    def generate_query_based_error():
        return "ERRORE: nessuno dei termini inseriti è valido, impossibile generare il riassunto"
