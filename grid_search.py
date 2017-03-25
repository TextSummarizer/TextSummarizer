import summarizer as s
import summary_generator as sg
import rouge

# Set your paths
model_path = 'C:/Users/Peppo/Desktop/GoogleNews-vectors-negative300.bin'
summary_destination_root = 'C:/grid-search/'
script_path = 'C:/Users/Peppo/Desktop/w2vm/rouge4MultiLing/rouge/ROUGE-1.5.5.pl'
data_path = 'C:/Users/Peppo/Desktop/w2vm/rouge4MultiLing/rouge/data'
gold_standard_path = 'C:/training/summary/'
results_path = 'grid-search-results.txt'
training_body_path = 'C:/training/body/'
training_length_path = 'C:/training/length.txt'

# Set your ranges
tfidf_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
redundancy_values = [0.8, 0.85, 0.9, 0.95]

# Init my summarizer
print 'Loading model...'
s = s.Summarizer(model_path=model_path)
print 'done\n'

# Generate summaries for all parameters combinations
for tfidf_value in tfidf_values:
    print 'Summarization with tdidf ' + str(tfidf_value) + '...'

    for redundancy_value in redundancy_values:
        # Update summarizer's configuration
        tfidf_str = "".join(str(tfidf_value).split("."))
        redundancy_str = "".join(str(redundancy_value).split("."))

        # Generate new name for the destination directory
        new_dir = 'tfidf_' + str(tfidf_str) + "_redundancy_" + str(redundancy_str)
        destination_path = summary_destination_root + new_dir

        # Run summary generation process
        gen = sg.SummaryGenerator(body_dir_path=training_body_path,
                                  target_length_path=training_length_path,
                                  destination_path=destination_path)
        gen.run(s, tfidf_threshold=tfidf_value, redundancy_threshold=redundancy_value)

print "ok.\n"

print 'Grid search on summaryes with ROUGE metrics: STARTED!'
rouge.compute(tfidf_values=tfidf_values,
              redundancy_values=redundancy_values,
              results_path=results_path,
              script_path=script_path,
              data_path=data_path,
              summary_destination_path=summary_destination_root,
              gold_standard_path=gold_standard_path)
print "Everything done. Now go to your result path and see results. Bye!"
