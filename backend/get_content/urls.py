from django.urls import path
from .views import DataAPIView, LoginAPIView, RegistrationAPIView, SettingsProfile, InfoAPIView, SearchAPIView, ScoreAPIView, IsWatched, AnimeListAPIView, MyList, UserAPIView

urlpatterns = [
    path('api/data/<str:sort>/', DataAPIView.as_view(), name='data_api_view'),
    path('api/data/mylist/<int:id>/<str:sort>/', MyList.as_view(), name='data_api_view'),
    path('api/info/anime/', InfoAPIView.as_view(), name='info_api_view'),
    path('api/anime/', IsWatched.as_view(), name='info_api_view'),
    path('api/search', SearchAPIView.as_view(), name='search_api_view'),
    path('api/login/', LoginAPIView.as_view(), name='login_api_view'),
    path('api/register/', RegistrationAPIView.as_view(), name='register_api_view'),
    path('api/settings/', SettingsProfile.as_view(), name='settings_profile'), 
    path('api/score/', ScoreAPIView.as_view(), name='info_api_view'),
    path('api/anime-list/', AnimeListAPIView.as_view(), name='anime_list_api_view'),
    path('api/user/<int:user_id>/', UserAPIView.as_view(), name='user_api'),
]
