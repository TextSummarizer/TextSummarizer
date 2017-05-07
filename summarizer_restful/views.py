from rest_framework import generics
from rest_framework import mixins
import json
from django.http import JsonResponse

import summarizer

s = summarizer.Summarizer(
    model_path="C:/Users/Gianni Mastroscianni/Desktop/Magistrale/Accesso Intelligente all'Informazione ed Elaborazione del Linguaggio Naturale/Progetto/word2vec_models/enwiki_20161220_skip_300.bin")


class Summary(generics.GenericAPIView, mixins.CreateModelMixin):
    def post(self, request):
        """
        text = str(request.POST.get('text'))
        redundancy_threshold = float(request.POST.get('redundancy_threshold'))
        tfidf = request.POST.get('tfidf_threshold')
        summary_length = float(request.POST.get('summary_length'))
        print type(tfidf)
        if summary_length >= 1:
            summary_length = int(summary_length) #controllo: num frasi riassunto > num frasi testo, escape sull' " e '

        query_based_token = request.POST.get('query_based_token')  # controlli

        s.set_tfidf_threshold(tfidf)
        s.set_redundancy_threshold(redundancy_threshold)
        summary, error_msg, boolean = s.summarize(text, summary_length, query_based_token)
        to_return = {'summary': summary, 'error': error_msg, 'query_token_error': boolean}
        return JsonResponse(to_return)"""

        js = '{"text": "Jovon Johnson (born November 2, 1983) is an American player of Canadian football as a defensive back for the Montreal Alouettes of the Canadian Football League (CFL). Johnson was the winner of the CFLs Most Outstanding Defensive Player Award in 2011 while with the Winnipeg Blue Bombers, becoming the first defensive back to win the award in the league. He is also a two-time CFL All-Star and five-time CFL East Division All-Star. In addition, he was a member of the 2007 Saskatchewan Roughriders that won the Grey Cup, though he spent little time on the active roster and finished the penultimate game on the practice roster.",  "redundancy_threshold": 0.95,"tfidf_threshold": 0.2,"summary_length": 0.05, "query_based_token": ""}'

        data = json.loads(js)

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
