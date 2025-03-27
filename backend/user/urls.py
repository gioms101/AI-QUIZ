from django.urls import path
from .views import RegisterUserAPIView, CheckAuthentication


urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name="user-register"),
    path('check-auth/', CheckAuthentication.as_view(), name="check-auth"),
]
