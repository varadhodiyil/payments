import stripe
from django.conf import settings


STRIPE_API_KEY = getattr(settings, 'STRIPE_API_KEY', None)

if STRIPE_API_KEY is None:
    raise ValueError("Stripe Key Not Set")


stripe.api_key = STRIPE_API_KEY


def create_customer(user):
    result = stripe.Customer.create(
        description="Customer creation for recurring payment",
        name="{0} {1}" .format(user.last_name, user.first_name),
        email=user.email
    )
    return result['id']


def create_payment_method(card):
    try:
        result = stripe.PaymentMethod.create(
            type="card",
            card=card
        )
        return True, result['id'], result['card']['last4'] , result['card']['brand']
    except Exception as e:
        return False, e, "" , ""


def attach_source(customer, source):
    stripe.PaymentMethod.attach(
        source,
        customer=customer,
    )


def set_default(customer, card_id):
    stripe.Customer.modify(
        customer,
        invoice_settings={"default_payment_method": card_id},
    )


def create_subscription(customer, price=""):
	sub = stripe.Subscription.create(
		customer=customer,
		items=[
			{"price": price},
		],
	)
	return sub['id']
