from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=140)
    desc = models.CharField(max_length=512)
    creation_date = models.DateTimeField(auto_now=True)

class Image(models.Model):
    name = models.CharField(max_length=140)
    desc = models.CharField(max_length=512)
    creation_date = models.DateTimeField(auto_now=True)
    source = models.URLField()
    tags = models.ManyToManyField(Tag)
