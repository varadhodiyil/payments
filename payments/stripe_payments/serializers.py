from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta


class PaymentMethodSerializer(serializers.Serializer):
	number = serializers.CharField(max_length=20)
	exp_month = serializers.IntegerField(min_value=1, max_value=12)
	exp_year = serializers.IntegerField(min_value=timezone.now().strftime(
		"%y"), max_value=(timezone.now() + timedelta(weeks=520)).strftime("%y"))
	cvc = serializers.IntegerField(max_value=9999)
