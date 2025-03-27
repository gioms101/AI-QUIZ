from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserRegisterSerializer


class RegisterUserAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer


class CheckAuthentication(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # If the request reaches here, the token is valid (due to IsAuthenticated)
        return Response({'status': 'authenticated'})
