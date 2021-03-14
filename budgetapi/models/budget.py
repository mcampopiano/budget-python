from django.db import models
from rest_framework.authtoken.models import Token

class Budget(models.Model):
    user = models.ForeignKey(Token, on_delete=models.CASCADE)
    month = models.CharField(max_length=15)
    year = models.CharField(max_length=4)
    est_income = models.FloatField()


    @property
    def actual_inc(self):
        return self.__actual_inc

    @actual_inc.setter
    def actual_inc(self, value):
        self.__actual_inc = value

    @property
    def total_budget(self):
        return self.__total_budget

    @total_budget.setter
    def total_budget(self, value):
        self.__total_budget = value
