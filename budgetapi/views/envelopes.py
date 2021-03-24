"""View module for handling requests about envelopes"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from budgetapi.models import Envelope, GeneralExpense
from django.db.models import Sum

class Envelopes(ViewSet):
    def create(self, request):
        token = Token.objects.get(user = request.auth.user)
        envelope = Envelope()
        envelope.name = request.data['name']
        envelope.user = token
        envelope.budget=request.data['budget']
        envelope.is_active=True

        try:
            envelope.save()
            serializer = EnvelopeSerializer(envelope, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        envelopes = Envelope.objects.all()
        for envelope in envelopes:            
            try:
                payments = GeneralExpense.objects.filter(envelope = envelope)
                payment_total=payments.aggregate(Sum('amount'))
                envelope.total = round(payment_total['amount__sum'], 2)
            except GeneralExpense.DoesNotExist:
                envelope.total = 0

        serializer = EnvelopeSerializer(envelopes, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        envelope = Envelope.objects.get(pk=pk)

        token = Token.objects.get(user = request.auth.user)
        envelope.name = request.data['name']
        envelope.user = token
        envelope.budget=request.data['budget']
        envelope.is_active=True

        envelope.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            envelope = Envelope.objects.get(pk=pk)
            envelope.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Envelope.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        envelope = Envelope.objects.get(pk=pk)

        try:
            payments = GeneralExpense.objects.filter(envelope = envelope)
            payment_total=payments.aggregate(Sum('amount'))
            envelope.total = round(payment_total['amount__sum'], 2)
        except GeneralExpense.DoesNotExist:
            envelope.total = 0

        serializer = EnvelopeSerializer(envelope, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=True)
    def purchases(self, request, pk=None):
        if request.method == "POST":
            envelope = Envelope.objects.get(pk=pk)
            purchase = GeneralExpense()
            purchase.budget_id = request.data['budgetId']
            purchase.envelope = envelope
            purchase.location = request.data['location']
            purchase.date = request.data['date']
            purchase.amount = request.data['amount']

            purchase.save()
            return Response({}, status=status.HTTP_201_CREATED)
        
        elif request.method == "DELETE":
            try:
                purchase = GeneralExpense.objects.get(pk=pk)
                purchase.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except GeneralExpense.DoesNotExist:
                return Response(
                    {'message': 'Event does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )







class EnvelopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envelope
        fields = ('id', 'name', 'user', 'budget', 'is_active', 'payment', 'total')
        depth = 1