from rest_framework import generics
from rest_framework import mixins
import json
from django.http import JsonResponse

import summarizer

s = summarizer.Summarizer(
    model_path="C:/Users/Gianni Mastroscianni/Desktop/Magistrale/Accesso Intelligente all'Informazione ed Elaborazione del Linguaggio Naturale/Progetto/word2vec_models/enwiki_20161220_skip_300.bin")


class Summary(generics.GenericAPIView, mixins.CreateModelMixin):
    def post(self, request):
        data = json.loads(request.body)                             #controllo:  escape sull' " e '
                                                                    # problemi con l'italiano(lettere accentate):
                                                                    # 'utf8' codec can't decode byte 0xe8 in position 34: invalid continuation/start byte
                                                                    # e credo che i riassunti li genereremo su testi in italiano

        text = data['text']
        redundancy_threshold = data['redundancy_threshold']
        tfidf = data['tfidf_threshold']
        summary_length = data['summary_length']
        query_based_token = data['query_based_token']

        s.set_tfidf_threshold(tfidf)
        s.set_redundancy_threshold(redundancy_threshold)
        summary, error_msg, boolean = s.summarize(text, summary_length, query_based_token)
        to_return = {'summary': summary, 'error': error_msg, 'query_token_error': boolean}

        return JsonResponse(to_return)
