import stripe
from django.conf import settings
from django.utils import timezone
from payments.stripe_payments import models
from datetime import datetime

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
        return True, result['id'], result['card']['last4'], result['card']['brand']
    except Exception as e:
        return False, e, "", ""


def attach_source(customer, source):
    """
            Attaches source to customer
    """
    stripe.PaymentMethod.attach(
        source,
        customer=customer,
    )


def set_default(customer, card_id):
    """
            Set's payment source as default.
    """
    stripe.Customer.modify(
        customer,
        invoice_settings={"default_payment_method": card_id},
    )


def create_subscription(customer, price="price_1Hyh1JBjPTNvMQM4Y3qfuo6o"):
    """
            Creates subscription for user
    """
    if price is None:
        price = "price_1Hyh1JBjPTNvMQM4Y3qfuo6o"

    try:
        sub = stripe.Subscription.create(
            customer=customer,
            items=[
                {"price": price},
            ],
        )
        return True, sub['id'], price
    except Exception as e:
        return False, e, ""


def get_event(data):
    try:

        return stripe.Event.construct_from(
            data, stripe.api_key
        )
    except ValueError:
        return None


def update_payment_status(subscription, status):
    _id = subscription.get('id', None)
    _created = subscription.get('created', timezone.now().timestamp())
    _dt_object = datetime.fromtimestamp(_created)
    _stripe_user = subscription.get('customer', None)

    _dt_object = timezone.make_aware(_dt_object)
    models.Payments.objects.filter(transaction_id=_id).update(
        status=status, transaction_updated=_dt_object)

    customer = models.StripeCustomer.objects.filter(stripe_user=_stripe_user)
    if customer.count() > 0:
        customer = customer.get()
        models.Events(event_id=_id, customer=customer, event_status=status,
                      event_time=_dt_object).save()
    return True
