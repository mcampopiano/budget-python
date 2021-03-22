from django.db from django.db import models

class Payment(models.Model):
    recurring_bill = models.ForeignKey("RecurringBill")
    budget = models.ForeignKey("Budget")
    amount = models.FloatField()
    date_paid = models.DateField(auto_now=False, auto_now_add=False)