from django.urls import path
from .views import DataAPIView, LoginAPIView, RegistrationAPIView, SettingsProfile, CheckEmailAPIView, CheckUsernameAPIView, InfoAPIView, SearchAPIView, ScoreAPIView, IsWatched, AnimeListAPIView, MyList, Recommendations_CBF

urlpatterns = [
    path('api/data/<str:sort>/', DataAPIView.as_view(), name='data_api_view'),
    path('api/data/mylist/<int:id>/<str:sort>/', MyList.as_view(), name='data_api_view'),
    path('api/info/anime/', InfoAPIView.as_view(), name='info_api_view'),
    path('api/rec/anime/', Recommendations_CBF.as_view(), name='info_api_view'),
    path('api/anime/', IsWatched.as_view(), name='info_api_view'),
    path('api/search', SearchAPIView.as_view(), name='search_api_view'),
    path('api/login/', LoginAPIView.as_view(), name='login_api_view'),
    path('api/register/', RegistrationAPIView.as_view(), name='register_api_view'),
    path('api/settings/', SettingsProfile.as_view(), name='settings_profile'),
    path('api/check-email/', CheckEmailAPIView.as_view(), name='check_email_api_view'),
    path('api/check-username/', CheckUsernameAPIView.as_view(), name='check_username_api_view'),  
    path('api/score/', ScoreAPIView.as_view(), name='info_api_view'),
    path('api/anime-list/', AnimeListAPIView.as_view(), name='anime_list_api_view'),
]
