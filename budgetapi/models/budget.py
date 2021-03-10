from django.db import models
from rest_framework.authtoken.models import Token

class Budget(models.Model):
    user = models.ForeignKey(Token, on_delete=models.CASCADE)
    month = models.CharField(max_length=15)
    year = models.CharField(max_length=4)
    est_income = models.FloatField()
