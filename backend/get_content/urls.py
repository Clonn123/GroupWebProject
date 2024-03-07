from django.urls import path
from .views import DataAPIView, LoginAPIView, RegistrationAPIView, SettingsProfile, CheckEmailAPIView, CheckUsernameAPIView, InfoAPIView, SearchAPIView

urlpatterns = [
    path('api/data/<str:sort>/', DataAPIView.as_view(), name='data_api_view'),
    path('api/info/anime/<int:anime_id>/', InfoAPIView.as_view(), name='info_api_view'),
    path('api/search', SearchAPIView.as_view(), name='search_api_view'),
    path('api/login/', LoginAPIView.as_view(), name='login_api_view'),
    path('api/register/', RegistrationAPIView.as_view(), name='register_api_view'),
    path('api/settings/', SettingsProfile.as_view(), name='settings_profile'),
    path('api/check-email/', CheckEmailAPIView.as_view(), name='check_email_api_view'),
    path('api/check-username/', CheckUsernameAPIView.as_view(), name='check_username_api_view'),
]
