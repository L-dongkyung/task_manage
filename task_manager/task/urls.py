from django.urls import path
from task.views import (
    TaskRegistrationCreateAPIView,
    TaskUpdateAPIView,
    SubTaskCompleteAPIView,
)

from . import views

urlpatterns = [
    path('task/', TaskRegistrationCreateAPIView.as_view(), name="create"),
    path('task/<int:pk>', TaskUpdateAPIView.as_view(), name='update'),
    path('subtask/<int:pk>', SubTaskCompleteAPIView.as_view(), name='complete')
]
