"""View module for handling requests about deposits"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from budgetapi.models import Deposit, Budget
from django.db.models import Sum

class Deposits(ViewSet):
    def create(self, request):
        deposit = Deposit()
        deposit.budget = request.data['budgetId']
        deposit.source = request.data['source']
        deposit.amount = request.data['amount']
        deposit.date = request.data['date']

        deposit.save()
        serializer = depositSerializer(deposit, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class depositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['budget', 'source', 'amount', 'date']