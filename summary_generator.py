import os, data


class SummaryGenerator:

    def __init__(self, body_dir_path, target_length_path, destination_path):
        self.body_dir_path = body_dir_path
        self.target_length_path = target_length_path
        self.destination_path = destination_path

    @staticmethod
    def _read_len(target_length_path):
        res_map = {}
        f = open(target_length_path, "r")
        lines = f.readlines()

        for line in lines:
            l = line[:len(line) - 1]
            l = l.split(",")
            res_map[l[0]] = int(l[1])

        return res_map

    def run(self, summarizer, tfidf_threshold, redundancy_threshold):
        # Read summary's target lengths. Store them in a map (file_name -> target_length)
        len_map = self._read_len(self.target_length_path)

        # Set up the summarizer
        summarizer.set_tfidf_threshold(tfidf_threshold)
        summarizer.set_redundancy_threshold(redundancy_threshold)

        # Iterate over text directory and use the model to generate summaries
        for filename in os.listdir(self.body_dir_path):
            print "Processing " + filename
            summary_length = len_map[filename]
            summary = summarizer.summarize(self.body_dir_path + filename, summary_length)
            data.export_summary(output_dir_path=self.destination_path, filename=filename, text=summary)
