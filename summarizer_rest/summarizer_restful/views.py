from models import Document
from serializers import DocumentSerializer
from rest_framework import generics
import summarizer
from rest_framework import mixins


class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class DocumentDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    # qui dovremmo eseguire il nostro codice

    def summarize(self, pk):
        obj = self.get(pk)
        s = summarizer.Summarizer(
            model_path="C:/Users/Gianni Mastroscianni/Desktop/Magistrale/Accesso Intelligente all'Informazione ed Elaborazione del Linguaggio Naturale/Progetto/word2vec_models/enwiki_20161220_skip_300",
            regex=True)
        summary = s.summarize(obj.doc, obj.summary_length)
        obj.summary = summary
