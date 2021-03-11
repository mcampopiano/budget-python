"""View module for handling requests about envelopes"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from budgetapi.models import Envelope

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

class EnvelopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envelope
        fields = ('id', 'name', 'user', 'budget', 'is_active')