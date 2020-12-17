from django.contrib.auth import authenticate
from payments.stripe_payments import models, serializers
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from payments.stripe_payments import stripe_service


class CreatePaymentMethod(GenericAPIView):
	serializer_class = serializers.PaymentMethodSerializer

	def get(self, request, *args, **kwargs):

		return Response()


	def post(self, request,*args, **kwargs):

		return Response()
