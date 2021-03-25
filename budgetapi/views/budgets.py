"""View module for handling requests about budgets"""
from typing import Type
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from budgetapi.models import Budget, Deposit, Envelope, GeneralExpense, RecurringBill, Payment
from django.db.models import Sum


class Budgets(ViewSet):
    """Monthly budgets"""

    def create(self, request):
       
        token = Token.objects.get(user = request.auth.user)
        budget = Budget()
        budget.user_id = token
        budget.month = request.data["month"]
        budget.year = request.data["year"]
        budget.est_income = request.data["estIncome"]

        try:
            budget.save()
            serializer = BudgetSerializer(budget, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        budgets = Budget.objects.all()
        
        for budget in budgets:
            budget.actual_inc = 0

            try:
                income = Deposit.objects.filter(budget=budget)
                total_income = income.aggregate(Sum('amount'))
                if total_income['amount__sum'] is not None:
                    budget.actual_inc = total_income['amount__sum']
            except Deposit.DoesNotExist:
                budget.actual_inc = 0

            try:
                token = Token.objects.get(user=request.auth.user)
                related_envelopes = Envelope.objects.filter(is_active=True, user_id=budget.user_id)
                related_bills = RecurringBill.objects.filter(user = token)
                related_bills = related_bills.aggregate(Sum('expected_amount'))
                total_budget = related_envelopes.aggregate(Sum('budget'))
                try:
                    total_budget = total_budget['budget__sum'] + related_bills['expected_amount__sum']
                except TypeError:
                    if total_budget['budget__sum'] is not None:
                        total_budget = total_budget['budget__sum']
                    elif related_bills['expected_amount__sum'] is not None:
                        total_budget = related_bills['expected_amount__sum']
                    else:
                        total_budget = 0
                try:
                    total_spent = 0
                    bill_payments = Payment.objects.filter(budget = budget)
                    bill_payments = bill_payments.aggregate(Sum('amount'))
                    total_spent = total_spent + bill_payments['amount__sum']
                except TypeError:
                    total_spent = 0
                for envelope in related_envelopes:
                    payments = GeneralExpense.objects.filter(envelope = envelope, budget = budget)
                    try:
                        payment_total=payments.aggregate(Sum('amount'))
                        total_spent += payment_total['amount__sum']
                    except TypeError:
                        total_spent = 0
                budget.total_budget = round(total_budget, 2)
                budget.total_spent = round(total_spent, 2)
                budget.remaining_budget = round((total_budget - total_spent), 2)
                budget.net_total = round((budget.actual_inc - total_spent), 2)
            except Envelope.DoesNotExist:
                budget.total_budget = 0
            except RecurringBill.DoesNotExist:
                pass

        serializer = BudgetSerializer(budgets, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        budget = Budget.objects.get(pk=pk)
        budget.actual_inc = 0

        try:
            income = Deposit.objects.filter(budget_id=pk)
            total_income = income.aggregate(Sum('amount'))
            if total_income['amount__sum'] != None:
                budget.actual_inc = total_income['amount__sum']
        except Deposit.DoesNotExist:
            budget.actual_inc = 0

        try:
            token = Token.objects.get(user=request.auth.user)
            related_envelopes = Envelope.objects.filter(is_active=True, user_id=budget.user_id)
            related_bills = RecurringBill.objects.filter(user = token)
            related_bills = related_bills.aggregate(Sum('expected_amount'))
            total_budget = related_envelopes.aggregate(Sum('budget'))
            try:
                total_budget = total_budget['budget__sum'] + related_bills['expected_amount__sum']
            except TypeError:
                if total_budget['budget__sum'] is not None:
                    total_budget = total_budget['budget__sum']
                elif related_bills['expected_amount__sum'] is not None:
                    total_budget = related_bills['expected_amount__sum']
                else:
                    total_budget = 0
            try:
                total_spent = 0
                bill_payments = Payment.objects.filter(budget = budget)
                bill_payments = bill_payments.aggregate(Sum('amount'))
                total_spent = total_spent + bill_payments['amount__sum']
            except TypeError:
                total_spent = 0
            for envelope in related_envelopes:
                payments = GeneralExpense.objects.filter(envelope = envelope, budget = budget)
                try:
                    payment_total=payments.aggregate(Sum('amount'))
                    total_spent += payment_total['amount__sum']
                except TypeError:
                    total_spent = 0
            budget.total_budget = round(total_budget, 2)
            budget.total_spent = round(total_spent, 2)
            budget.remaining_budget = round((total_budget - total_spent), 2)
            budget.net_total = round((budget.actual_inc - total_spent), 2)
        except Envelope.DoesNotExist:
            budget.total_budget = 0
        except RecurringBill.DoesNotExist:
            pass
        try:
            serializer = BudgetSerializer(budget, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Budget.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
           
            


class BudgetSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Budget
        fields = ('id', 'user', 'month', 'year', 'est_income', 'income', 'actual_inc', 'total_budget', 
        'total_spent', 'remaining_budget', 'net_total')
        depth = 1