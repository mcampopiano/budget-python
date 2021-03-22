from django.db import models

class Payment(models.Model):
    recurring_bill = models.ForeignKey("RecurringBill", on_delete=models.CASCADE, related_name="payments")
    budget = models.ForeignKey("Budget", on_delete=models.CASCADE)
    amount = models.FloatField()
    date_paid = models.DateField(auto_now=False, auto_now_add=False)