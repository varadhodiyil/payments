from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from payments.stripe_payments.models import StripeCustomer, CustomerCard
from django.shortcuts import get_object_or_404
from payments.stripe_payments import stripe_service
from rest_framework.validators import ValidationError



class PaymentCardSerializer(serializers.ModelSerializer):

	class Meta:
		fields = '__all__'
		model = CustomerCard


class PaymentMethodSerializer(serializers.Serializer):
	number = serializers.IntegerField(max_value=99999999999999999999)
	exp_month = serializers.IntegerField(min_value=1, max_value=12)
	exp_year = serializers.IntegerField(min_value=int(timezone.now().strftime(
		"%Y")), max_value=int((timezone.now() + timedelta(weeks=520)).strftime("%Y")))
	cvc = serializers.IntegerField(max_value=9999)

	def save(self, user):
		customer = StripeCustomer.objects.filter(user=user)
		status = False
		if len(customer) > 0:
			customer = get_object_or_404(customer)
		else:
			customer = StripeCustomer(user=user,stripe_user= stripe_service.create_customer(user))
			customer.save()
			status = True

		card_status , card , last4 , brand = stripe_service.create_payment_method(self.validated_data)
		if not card_status:
			raise ValidationError( {'status': False, 'message': card})


		stripe_service.attach_source(customer.stripe_user , card)


		_card = CustomerCard(user=user,card_id=card,last4=last4 ,is_default=status , brand= brand)
		_card.save()

		if status:
			stripe_service.set_default(customer.stripe_user , card)
		return status , customer



class SetDefaultSerializer(serializers.Serializer):
	card = serializers.CharField(max_length=100)

	def save(self,user):
		has_card = CustomerCard.objects.filter(user= user , card_id= self.validated_data['card'])
		if len(has_card) == 0:
			raise ValidationError({'status': False, 'message': 'No Such card found'})
		stripe_user = StripeCustomer.objects.get(user =user)
		stripe_service.set_default(stripe_user.stripe_user , self.validated_data['card'])
		CustomerCard.objects.filter(user= user).update(is_default=False)
		has_card.update(is_default=True)
		return True


