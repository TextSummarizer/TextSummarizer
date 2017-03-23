import os


class SummaryGenerator:

    def __init__(self, body_dir_path, result_dir_path):
        self.body_dir_path = body_dir_path

    @staticmethod
    def _read_len(len_file_path):
        res_map = {}
        f = open(len_file_path, "r")
        lines = f.readlines()

        for line in lines:
            l = line[:len(line) - 1]
            l = l.split(",")
            res_map[l[0]] = int(l[1])

        return res_map

    def run(self, len_path, model_path, stemming, remove_stopword, tfidf_threshold, redundancy_threshold):
        import summarizer
        s = summarizer.Summarizer(model_path,
                                  stemming,
                                  remove_stopword,
                                  tfidf_threshold,
                                  redundancy_threshold)

        len_map = self._read_len(len_path)

        for filename in os.listdir(self.body_dir_path):
            summary_length = len_map[filename]
            s.summarize(self.body_dir_path + filename, summary_length)


s = SummaryGenerator('C:/Users/Peppo/Desktop/prova', 'C:/Users/Peppo/Desktop/prova')
print s.run('C:/Users/Peppo/Desktop/len/en.txt')
