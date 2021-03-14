from django.db import models

class Deposit(models.Model):
    budget=models.ForeignKey("Budget", on_delete=models.CASCADE, related_name="income")
    source=models.CharField(max_length=50)
    amount=models.FloatField()
    date=models.DateTimeField(auto_now=False, auto_now_add=False)