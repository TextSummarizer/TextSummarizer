import summarizer as s
import summary_generator as sg


tfidf_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
redundancy_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

# Init my summarizer
s = s.Summarizer(model_path='C:/Users/Peppo/Desktop/GoogleNews-vectors-negative300.bin')
print "Model loaded"

# Grid search though all parameters combinations
for tfidf_value in tfidf_values:
    for redundancy_value in redundancy_values:
        # Update summarizer's configuration
        tfidf_str = "".join(str(tfidf_value).split("."))
        redundancy_str = "".join(str(redundancy_value).split("."))

        # Generate new name for the destination directory
        new_dir = 'tfidf_' + str(tfidf_str) + "_redundancy_" + str(redundancy_str)
        destination_path = 'C:/grid-search/' + new_dir

        # Run summary generation process
        gen = sg.SummaryGenerator(body_dir_path='C:/training/body/',
                                  target_length_path='C:/training/length.txt',
                                  destination_path=destination_path)
        gen.run(s, tfidf_threshold=tfidf_value, redundancy_threshold=redundancy_value)

print "done."
