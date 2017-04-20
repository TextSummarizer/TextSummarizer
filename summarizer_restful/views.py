from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response

import summarizer

s = summarizer.Summarizer(
    model_path="C:/Users/Gianni Mastroscianni/Desktop/Magistrale/Accesso Intelligente all'Informazione ed Elaborazione del Linguaggio Naturale/Progetto/word2vec_models/enwiki_20161220_skip_300.bin",
    regex=True)


class Summary(generics.GenericAPIView, mixins.RetrieveModelMixin):
    def get(self, request):
        text = str(request.query_params.get('text'))
        print request.data
        print text
        redundancy_threshold = request.query_params.get('redundancy_threshold')
        tfidf = request.query_params.get('tfidf')
        summary_length = request.query_params.get('summary_length')

        s.set_tfidf_threshold(tfidf)
        s.set_redundancy_threshold(redundancy_threshold)
        summary = s.summarize(text, summary_length)

        return Response(summary)
