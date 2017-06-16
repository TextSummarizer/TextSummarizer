# coding=utf-8

from rest_framework import generics
from rest_framework import mixins
import json
from django.http import JsonResponse

import summarizer

s = summarizer.Summarizer(
    model_path="itwiki_20161220_skip_300.bin")


class Summary(generics.GenericAPIView, mixins.CreateModelMixin):
    def post(self, request):
        # load json
        data = json.loads(request.body)

        list = []

        redundancy_threshold = data['redundancy_threshold']
        tfidf = data['tfidf_threshold']
        summary_length = data['summary_length']
        query_based_token = data['query_based_token']

        s.set_tfidf_threshold(tfidf)
        s.set_redundancy_threshold(redundancy_threshold)
        for object in data['documents']:
            name = object['id']
            text = object['text']
            summary, error_msg, boolean = s.summarize(text, summary_length, query_based_token)
            to_return = {'id': name, 'summary': summary, 'error': error_msg, 'query_token_error': boolean}
            list.append(to_return)

        print JsonResponse(list)
