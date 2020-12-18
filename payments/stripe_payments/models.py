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


class Payments(models.Model):
	objects = models.Manager()

	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	card = models.ForeignKey(CustomerCard,on_delete=models.DO_NOTHING)
	created_at = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=50)
	transaction_id = models.CharField(max_length=100)
	price = models.CharField(max_length=50)
	transaction_updated = models.DateTimeField(null=True,blank=True)


class Events(models.Model):
	objects = models.Manager()

	id = models.AutoField(primary_key=True)

	event_id = models.CharField(max_length=100)
	customer = models.ForeignKey(StripeCustomer,on_delete=models.DO_NOTHING)
	event_time = models.DateTimeField()
	event_status = models.CharField(max_length=100)
	