from rest_framework import serializers
from payments.users import models

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		fields = ['username','first_name','last_name','email','password']
		model = models.User
