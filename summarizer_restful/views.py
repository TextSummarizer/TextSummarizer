from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response

import summarizer

s = summarizer.Summarizer(
    model_path="C:/Users/Gianni Mastroscianni/Desktop/Magistrale/Accesso Intelligente all'Informazione ed Elaborazione del Linguaggio Naturale/Progetto/word2vec_models/enwiki_20161220_skip_300.bin")


class Summary(generics.GenericAPIView, mixins.CreateModelMixin):
    def post(self, request):
        text = str(request.POST.get('text'))
        redundancy_threshold = float(request.POST.get('redundancy_threshold'))
        tfidf = float(request.POST.get('tfidf_threshold'))
        summary_length = float(request.POST.get('summary_length'))  # che casting?

        if summary_length >= 1:
            summary_length = int(summary_length)

        query_based_token = request.POST.get('query_based_token')  # controlli

        s.set_tfidf_threshold(tfidf)
        s.set_redundancy_threshold(redundancy_threshold)
        summary, error_msg, boolean = s.summarize(text, summary_length, query_based_token)
        to_return = {'summary': summary, 'error': error_msg, 'query_token_error': boolean}
        return Response(to_return)
