"""View module for handling requests about recurring bills"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from budgetapi.models import Envelope, GeneralExpense, RecurringBill
from django.db.models import Sum


class RecurringBills(ViewSet):
    def list(self, request):
        bills = RecurringBill.objects.all()

        serializer = RecurringBillSerializer(bills, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecurringBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringBill
        fields = ('id', 'user', 'biller', 'expected_amount', 'due_date')