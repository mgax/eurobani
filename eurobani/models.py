from django.db import models
from django.contrib.postgres.fields import JSONField

class Contract(models.Model):
    data = JSONField()

class Payment(models.Model):
    data = JSONField()
