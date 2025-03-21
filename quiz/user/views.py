from rest_framework.generics import CreateAPIView
from .serializers import UserRegisterSerializer


class RegisterUserAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
