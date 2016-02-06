from django.db import models

class Sample(models.Model):

    field1 = models.CharField(max_length=10)
    field2 = models.IntegerField()
