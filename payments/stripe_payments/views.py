from django.contrib.auth import authenticate
from payments.stripe_payments import models, serializers
from rest_framework import status
from rest_framework.generics import GenericAPIView , ListAPIView
from rest_framework.response import Response
from payments.stripe_payments import stripe_service
from payments.pagination import StandardResultsSetPagination

class CreatePaymentMethod(GenericAPIView):

	"""
		Creates Payment Card and attaches it to Stripe Customer
	"""
	serializer_class = serializers.PaymentMethodSerializer

	def post(self, request,*args, **kwargs):

		"""
			Valid card is required, to Save and auth token required
		"""
		data = request.data
		result = dict()
		if request.user.is_authenticated:
			s = self.get_serializer(data=data)
			if s.is_valid():
				status, customer = s.save(request.user)
				result['status'] = True
				result['message'] = "Card Added SuccessFully!"
				_status = "Created" if status else "Updated"
				result['result'] = "User {0} {1}".format(customer.stripe_user , _status)
				return Response(result)
			else:
				result['status'] = False
				result['errors'] = s.errors
				return Response(result, status = status.HTTP_400_BAD_REQUEST)
		else:
			result['status'] = True
			result['message'] = "Not Logged In"
			return Response(result, status=status.HTTP_401_UNAUTHORIZED)


class CardDetails(ListAPIView):
	"""
		Returns Card details of customer, paginated
		If not logged in, returns Empty array
	"""

	pagination_class = StandardResultsSetPagination
	serializer_class = serializers.PaymentCardSerializer

	def get_queryset(self):
		if self.request.user.is_authenticated:
			return models.CustomerCard.objects.order_by("-created_at").filter(user=self.request.user)
		return []


class SetDefaultCard(GenericAPIView):

	"""
		Sets default card for customer.
	"""

	serializer_class = serializers.SetDefaultSerializer

	def post(self , request, *args, **kwargs):

		"""
			Requires card Id as parameter.
		"""
		result = dict()
		if request.user.is_authenticated:
			s = self.get_serializer(data = request.data)
			if s.is_valid():
				s.save(request.user)
				result['status'] = True
				return Response(result)
			else:
				result['status'] = False
				result['errors'] = s.errors
				return Response(result, status= status.HTTP_400_BAD_REQUEST)
		else:
			result['status'] = True
			result['message'] = "Not Logged In"
			return Response(result, status=status.HTTP_401_UNAUTHORIZED)