from django.contrib.auth import authenticate
from payments.auth_tokens import models, serializers
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class LoginAPI(GenericAPIView):

    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        """
                Login with creds, return Token
        """

        data = request.data
        s = self.get_serializer(data=data)
        result = dict()
        if s.is_valid():
            user = s.validated_data['user']
            models.Token.objects.filter(user=user).delete()
            token = models.Token(user=user)
            token.save()
            result['status'] = True
            result['result'] = token.key
            return Response(result)
        else:
            result['status'] = False
            result['errors'] = s.errors
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPI(GenericAPIView):

    serializer_class = serializers.ProfileSerializer

    def get(self, request, *args, **kwargs):

        result = dict()
        if request.user.is_authenticated:
            s = self.get_serializer(request.user)
            result['status'] = True
            result['result'] = s.data
            return Response(result)
        else:
            result['status'] = False
            result['mesage'] = "Not Logged In!"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)
