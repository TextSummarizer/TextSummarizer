from django.db import models


class Document(models.Model):
    title = models.TextField(default=None)
    text = models.TextField()
    summary_length = models.IntegerField()

    def __str__(self):
        return self.title


class Summary(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "Summaries"
