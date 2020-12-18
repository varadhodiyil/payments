from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from payments.users import serializers

class UserAPI(GenericAPIView):

	"""
		Registration API
	"""
	serializer_class = serializers.UserSerializer

	def post(self , request, *args, **kwargs):
		"""
			Creates User, if user already exists, returns 401
		"""

		s = self.get_serializer(data=request.data)
		result = dict()
		if s.is_valid():
			result['status'] = True
			user = s.save()
			user.set_password(s.validated_data['password'])
			user.save()
			return Response(result)
		else:
			result['status'] = False
			result['errors'] = s.errors
			return Response(result, status=status.HTTP_400_BAD_REQUEST)