from django.urls import path
from .views import DataAPIView, LoginAPIView

urlpatterns = [
    path('api/data/', DataAPIView.as_view(), name='data_api_view'),
    path('api/login/', LoginAPIView.as_view(), name='login_api_view'),
]
