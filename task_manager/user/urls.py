from django.urls import path
from user.views import UserRegistrationAPIView

from . import views

urlpatterns = [
    path('check/', views.health_check),
    path('user/', UserRegistrationAPIView.as_view(), name="list"),
]
