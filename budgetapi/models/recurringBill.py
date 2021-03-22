from django.db import models
from rest_framework.authtoken.models import Token

class RecurringBill(models.Model):
    user = models.ForeignKey(Token, on_delete=models.CASCADE)
    biller = models.CharField(max_length=250)
    expected_amount = models.FloatField()
    due_date = models.IntegerField()
