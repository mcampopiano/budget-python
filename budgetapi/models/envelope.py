from django.db import models
from rest_framework.authtoken.models import Token

class Envelope(models.Model):
    user = models.ForeignKey(Token, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    budget = models.FloatField()
    is_active = models.BooleanField()

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, value):
        self.__total = value