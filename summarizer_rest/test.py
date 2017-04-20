import summary_generator
import summarizer

print "Setting summarizer..."
s = summarizer.Summarizer(
    model_path="C:/Users/Gianni Mastroscianni/Desktop/Magistrale/Accesso Intelligente all'Informazione ed Elaborazione del Linguaggio Naturale/Progetto/word2vec_models/itwiki_20161220_skip_300.bin",
    regex=True)

print "Generating summaries..."
sg = summary_generator.SummaryGenerator(
    "C:/Users/Gianni Mastroscianni/Desktop/Magistrale/Accesso Intelligente all'Informazione ed Elaborazione del Linguaggio Naturale/Progetto/word2vec_models/multilingMss2015Eval/body/text/it/",
    "C:/Users/Gianni Mastroscianni/Desktop/Magistrale/Accesso Intelligente all'Informazione ed Elaborazione del Linguaggio Naturale/Progetto/word2vec_models/multilingMss2015Eval/target-length/it.txt",
    "C:/Users/Gianni Mastroscianni/Desktop/italian_summaries_300/"
)

sg.run(s, 0.2, 0.95)
print "done!"

