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
from budgetapi.models import RecurringBill, Payment
from django.db.models import Sum


class RecurringBills(ViewSet):
    def list(self, request):
        bills = RecurringBill.objects.all()

        serializer = RecurringBillSerializer(bills, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        token = Token.objects.get(user = request.auth.user)
        bill = RecurringBill()
        
        bill.user = token
        bill.biller = request.data['biller']
        bill.expected_amount = request.data['expectedAmount']
        bill.due_date = request.data['dueDate']

        bill.save()

        serializer = RecurringBillSerializer(bill, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', 'DELETE'], detail=True)
    def payments(self, request, pk=None):
        if (request.method == 'POST'):
            payment = Payment()
            biller = RecurringBill.objects.get(pk=pk)
            payment.recurring_bill = biller
            payment.budget_id = request.data['budgetId']
            payment.amount = request.data['amount']
            payment.date_paid = request.data['datePaid']

            payment.save()

            serializer = PaymentSerializer(payment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'amount', 'date_paid', 'budget_id')


class RecurringBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringBill
        fields = ('id', 'biller', 'user', 'expected_amount', 'due_date', 'payments')
        depth = 1