from django.urls import path
from task.views import TaskRegistrationCreateAPIView

from . import views

urlpatterns = [
    path('task/', TaskRegistrationCreateAPIView.as_view(), name="create"),
]
