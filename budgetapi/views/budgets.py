"""View module for handling requests about budgets"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from budgetapi.models import Budget, Deposit, Envelope, GeneralExpense
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

        serializer = BudgetSerializer(budgets, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        budget = Budget.objects.get(pk=pk)

        try:
            income = Deposit.objects.filter(budget_id=pk)
            total_income = income.aggregate(Sum('amount'))
            budget.actual_inc = total_income['amount__sum']
        except Deposit.DoesNotExist:
            budget.actual_inc = 0

        try:
            related_envelopes = Envelope.objects.filter(is_active=True, user_id=budget.user_id)
            total_budget = related_envelopes.aggregate(Sum('budget'))
            total_spent = 0
            for envelope in related_envelopes:
                payments = GeneralExpense.objects.filter(envelope = envelope)
                payment_total=payments.aggregate(Sum('amount'))
                try:
                    total_spent += payment_total['amount__sum']
                except TypeError:
                    pass
            budget.total_budget = total_budget['budget__sum']
            budget.total_spent = total_spent
            budget.remaining_budget = total_budget['budget__sum'] - total_spent
            budget.net_total = total_income['amount__sum'] - total_spent
        except Envelope.DoesNotExist:
            budget.total_budget = 0
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