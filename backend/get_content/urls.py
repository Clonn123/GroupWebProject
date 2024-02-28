from django.urls import path
from .views import DataAPIView, LoginAPIView, RegistrationAPIView, SettingsProfile

urlpatterns = [
    path('api/data/', DataAPIView.as_view(), name='data_api_view'),
    path('api/login/', LoginAPIView.as_view(), name='login_api_view'),
    path('api/register/', RegistrationAPIView.as_view(), name='register_api_view'),
    path('api/settings/', SettingsProfile.as_view()),
]
