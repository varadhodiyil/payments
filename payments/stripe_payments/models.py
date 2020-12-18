from django.db import models

from payments.users.models import User


class StripeCustomer(models.Model):
	objects = models.Manager()

	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	stripe_user = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now=True)


class CustomerCard(models.Model):
	objects = models.Manager()

	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete= models.CASCADE)
	card_id = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now=True)
	is_default = models.BooleanField()
	last4 = models.IntegerField()
	brand = models.CharField(max_length=250)