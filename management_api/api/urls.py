from django.urls import path

from .views import (
    TodoListApiView,
    TodoListApi2View,
)
urlpatterns = [
    path('api', TodoListApiView.as_view()),
    path('api2', TodoListApi2View.as_view()),
]