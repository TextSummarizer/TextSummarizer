## Python Framework for Extractive Text Summarization
Natural Language Processing project for Master's Degree in Computer Science (Machine Learning curriculum) @ [University of Bari](http://www.uniba.it/ricerca/dipartimenti/informatica).
Implementation based on paper "Centroid-based Text Summarization through Compositionality of Word Embeddings" accepted at MultiLing 
Workshop in EACL 2017

### Params description
* `text`: string to summarize
* `summary_length`: <br />
  if k < 1 then summarize k% of the original text <br />
  else if k >= 1 choose the k most relevant sentences of the original text
* `query_based_token`: It's a list. <br /> If you don't like tfidf/lda methods to generate summary, give us your relevant token and we try to generate the summary based on them (example: ["music", "rock"]). If this list is full, centroid_mode param will be ignored.

### Code usage:
```python
import summarizer
s = summarizer.Summarizer(model_path="model.bin")
text = "text to summarize"
summary, text_error, boolean_error = s.summarize(text=text, summary_length=3, query_based_token=[])
summary_query_based, text_error_query_based, boolean_error_query_based = s.summarize(text=text, summary_length=0.5, query_based_token=["music", "rock"])
```
