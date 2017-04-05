from django.db import models


class Document(models.Model):
    # id = models.AutoField()
    doc = models.FileField(default=None)
    summary_length = models.IntegerField()
    summary = models.TextField(default=None, blank=True)

    def __str__(self):
        return self.id
