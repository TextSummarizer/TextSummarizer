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
        summary_length = int(request.POST.get('summary_length')) #qui ho lasciato int
        query_based_token = str(request.POST.get('query_based_token'))

        s.set_tfidf_threshold(tfidf)
        s.set_redundancy_threshold(redundancy_threshold)
        summary = s.summarize(text, summary_length, query_based_token)
        to_return = {'summary': summary}
        return Response(to_return)
