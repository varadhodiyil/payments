from django.contrib import admin
from payments.stripe_payments import models


# Register your models here.
admin.site.register(models.CustomerCard)
admin.site.register(models.StripeCustomer)