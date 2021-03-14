"""View module for handling requests about budgets"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from budgetapi.models import Budget


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

    def list(self, request):
        budgets = Budget.objects.all()

        serializer = BudgetSerializer(budgets, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        budgets = Budget.objects.get(pk=pk)

        try:
            serializer = BudgetSerializer(budgets, many=False, context={'request': request})
            return Response(serializer.data)
        except Budget.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class BudgetSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Budget
        fields = ('id', 'user', 'month', 'year', 'est_income', 'income')
        depth = 1