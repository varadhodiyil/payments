from django.db import models

from payments.users.models import User


class StripeCustomer(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	stripe_user = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now=True)