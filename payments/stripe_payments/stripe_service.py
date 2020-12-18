import stripe
from django.conf import settings


STRIPE_API_KEY = getattr(settings, 'STRIPE_API_KEY' , None)

if STRIPE_API_KEY is None:
	raise ValueError("Stripe Key Not Set")


stripe.api_key = STRIPE_API_KEY


def create_customer(user):
	result = stripe.Customer.create(
 	 description="Customer creation for recurring payment",
	  name= "{0} {1}" .format(user.last_name, user.first_name),
	  email = user.email
	)
	return result['id']
