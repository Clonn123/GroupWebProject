from django.urls import path
from .views import DataAPIView, LoginAPIView, RegistrationAPIView, SettingsProfile, CheckEmailAPIView, CheckUsernameAPIView, UserDetailView

urlpatterns = [
    path('api/data/', DataAPIView.as_view(), name='data_api_view'),
    path('api/login/', LoginAPIView.as_view(), name='login_api_view'),
    path('api/register/', RegistrationAPIView.as_view(), name='register_api_view'),
    path('api/settings/', SettingsProfile.as_view(), name='settings_profile'),
    path('api/check-email/', CheckEmailAPIView.as_view(), name='check_email_api_view'),
    path('api/check-username/', CheckUsernameAPIView.as_view(), name='check_username_api_view'),
    path('api/user/<int:user_id>/', UserDetailView.as_view(), name='user_detail_api_view'),
]
