from models import Summary, Document
from rest_framework import viewsets
from serializers import DocumentSerializer, SummarySerializer


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class SummaryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer
