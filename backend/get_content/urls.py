from django.urls import path
from .views import DataAPIView, DelObject, LoginAPIView, RegistrationAPIView, SettingsProfile, InfoAPIView, SearchAPIView, ScoreAPIView, IsWatched, IsWatchedManga, AnimeListAPIView, MyList, Recommendations_CBF, UserAPIView, Recommendations_CBF_Manga, InfoMangaAPIView, DelMangaObject, MangaListAPIView, ScoreMangaAPIView, SearchMangaAPIView, DataMangaAPIView, MyListManga

urlpatterns = [
    path('api/data/<str:sort>/', DataAPIView.as_view(), name='data_api_view'),
    path('api/data-manga/<str:sort>/', DataMangaAPIView.as_view(), name='data_api_view'),
    path('api/data/mylist/<int:id>/<str:sort>/', MyList.as_view(), name='data_api_view'),
    path('api/data/mylist-manga/<int:id>/<str:sort>/', MyListManga.as_view(), name='data_api_view'),
    path('api/info/anime/', InfoAPIView.as_view(), name='info_api_view'),
    path('api/info/manga/', InfoMangaAPIView.as_view(), name='info_manga_api_view'),
    path('api/rec/anime/', Recommendations_CBF.as_view(), name='rec_api_view'),
    path('api/rec/manga/', Recommendations_CBF_Manga.as_view(), name='rec_manga_api_view'),
    path('api/anime/', IsWatched.as_view(), name='info_api_view'),
    path('api/manga/', IsWatchedManga.as_view(), name='info_manga_api_view'),
    path('api/search', SearchAPIView.as_view(), name='search_api_view'),
    path('api/search-manga', SearchMangaAPIView.as_view(), name='search_manga_api_view'),
    path('api/login/', LoginAPIView.as_view(), name='login_api_view'),
    path('api/register/', RegistrationAPIView.as_view(), name='register_api_view'),
    path('api/settings/', SettingsProfile.as_view(), name='settings_profile'), 
    path('api/score/', ScoreAPIView.as_view(), name='info_api_view'),
    path('api/score-manga/', ScoreMangaAPIView.as_view(), name='info_manga_api_view'),
    path('api/anime/del', DelObject.as_view(), name='info_api_view'),
    path('api/manga/del', DelMangaObject.as_view(), name='info_api_view'),
    path('api/anime-list/', AnimeListAPIView.as_view(), name='anime_list_api_view'),
    path('api/manga-list/', MangaListAPIView.as_view(), name='anime_list_api_view'),
    path('api/user/<int:user_id>/', UserAPIView.as_view(), name='user_api'),
]
