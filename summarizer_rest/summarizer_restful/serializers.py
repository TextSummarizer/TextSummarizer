from models import Document
from rest_framework import serializers


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('doc', 'summary_length', 'summary')


