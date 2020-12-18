import json

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from payments.pagination import StandardResultsSetPagination
from payments.stripe_payments import models, serializers, stripe_service
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response


class CreatePaymentMethod(GenericAPIView):

    """
            Creates Payment Card and attaches it to Stripe Customer
    """
    serializer_class = serializers.PaymentMethodSerializer

    def post(self, request, *args, **kwargs):
        """
                        Valid card is required, to Save and auth token required
        """
        data = request.data
        result = dict()
        if request.user.is_authenticated:
            s = self.get_serializer(data=data)
            if s.is_valid():
                _status, customer = s.save(request.user)
                result['status'] = True
                result['message'] = "Card Added SuccessFully!"
                __status = "Created" if _status else "Updated"
                result['result'] = "User {0} {1}".format(
                    customer.stripe_user, __status)
                return Response(result)
            else:
                result['status'] = False
                result['errors'] = s.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
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

    def post(self, request, *args, **kwargs):
        """
                Requires card Id as parameter.
        """
        result = dict()
        if request.user.is_authenticated:
            s = self.get_serializer(data=request.data)
            if s.is_valid():
                s.save(request.user)
                result['status'] = True
                return Response(result)
            else:
                result['status'] = False
                result['errors'] = s.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            result['status'] = True
            result['message'] = "Not Logged In"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)


class EventsAPI(ListAPIView):
    """
            Returns Events logged for customer
    """

    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.EventsSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return models.Events.objects.filter(customer__user=self.request.user).order_by("-event_time")
        return []


class CreateSubscription(GenericAPIView):

    serializer_class = serializers.CreateSubscriptionSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        result = dict()
        if request.user.is_authenticated:
            _subs = models.Payments.objects.filter(
                user=request.user).order_by("-created_at")

            _subs = serializers.PaymentsSerializer(_subs, many=True).data
            _subs = self.paginate_queryset(_subs)
            return self.get_paginated_response(_subs)
        else:
            result['status'] = False
            result['message'] = "UnAuthorized!"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        result = dict()
        if request.user.is_authenticated:
            s = self.get_serializer(data=request.data)
            if s.is_valid():
                s.save(request.user)
                result['status'] = True
                return Response(result)
            else:
                result['status'] = False
                result['errors'] = s.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            result['status'] = True
            result['message'] = "Not Logged In"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
def event_listener(request):
    payload = json.loads(request.body)
    event = None

    event = stripe_service.get_event(payload)
    if not event:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'customer.subscription.created':
        subscription = event.data.object
        stripe_service.update_payment_status(subscription, "Created")

    elif event.type == 'customer.subscription.deleted':
        subscription = event.data.object
        stripe_service.update_payment_status(subscription, "Deleted")

    elif event.type == 'customer.subscription.pending_update_applied':
        subscription = event.data.object
        stripe_service.update_payment_status(
            subscription, "Pending_Update_Applied")

    elif event.type == 'customer.subscription.pending_update_expired':
        subscription = event.data.object
        stripe_service.update_payment_status(
            subscription, "Pending_Update_Expired")

    elif event.type == 'customer.subscription.trial_will_end':
        subscription = event.data.object
        stripe_service.update_payment_status(
            subscription, "Trial_Will_End")

    elif event.type == 'customer.subscription.updated':
        subscription = event.data.object
        stripe_service.update_payment_status(subscription, "Updated")

    elif event.type == 'invoice.payment_succeeded':
        subscription = event.data.object
        stripe_service.update_payment_status(subscription, "Payment Success")

    elif event.type == 'invoice.paid':
        subscription = event.data.object
        stripe_service.update_payment_status(subscription, "Invoice Paid")

    elif event.type == 'invoice.finalized':
        subscription = event.data.object
        stripe_service.update_payment_status(
            subscription, "Invoice Finalized!")

    return HttpResponse(status=200)
