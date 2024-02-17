from django.urls import path
from .views import MyAPIView

urlpatterns = [
    path('api/data/', MyAPIView.as_view(), name='my_api_view'),
]