"""
__author__ : Sathish Kumar John Peter
__email__ : sathishkumarb1139@gmail.com
__nationality__ : India
__date_created__ : 15/05/2020
"""

from django.db import models


# Create your models here.

class Store(models.Model):
    id = models.IntegerField(primary_key=True)
    index = models.IntegerField()
    date = models.TextField(null=True)
    channel = models.TextField(null=True)
    country = models.TextField(null=True)
    os = models.TextField(null=True)
    impressions = models.TextField(null=True,)
    clicks = models.IntegerField(null=True)
    installs = models.IntegerField(null=True)
    spend = models.FloatField(null=True)
    revenue = models.FloatField(null=True)

    class Meta:
        db_table = "store"

