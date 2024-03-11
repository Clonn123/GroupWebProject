from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Animes, Anime_info
from .models import Users
from .models import UserProfile
from .serializer import MyModelSerializer, InfoAnimeSerializer
from .serializer import UserModelSerializer
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.decorators import api_view
from datetime import datetime
from django.db.models import Q
import requests
import time
from urllib.parse import urlparse, parse_qs

# Users = get_user_model()

class DataAPIView(APIView): 
    def get(self, request, sort):
        if (sort == '-score' or sort == '-descriptionData' or sort == '-title_ru'
            or sort == 'score' or sort == 'descriptionData' or sort == 'title_ru'):
            data_list = Animes.objects.order_by(f'{sort}')
        else:
            data_list = Animes.objects.all()
            
            
        serializer = MyModelSerializer(data_list, many=True)
        return Response(serializer.data)
    
class InfoAPIView(APIView): 
    def get(self, request, anime_id):
        try:
            anime_info = Anime_info.objects.get(anime_id=anime_id)
            serializer = InfoAnimeSerializer(anime_info)
            
            anime_info2 = Animes.objects.get(anime_list_id=anime_id)
            serializer2 = MyModelSerializer(anime_info2)
            
            response_data = {
                "anime_info": serializer.data,
                "anime_info2": serializer2.data
            }
            return Response(response_data)
        except Anime_info.DoesNotExist or Animes.DoesNotExist:
            return Response({"message": "Anime not found"}, status=status.HTTP_404_NOT_FOUND)

class SearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        results = Animes.objects.filter(Q(title_en__startswith=query))
        serializer = MyModelSerializer(results, many=True)
        return Response(serializer.data)
class ScoreAPIView(APIView):
    def post(self, request):
        
        return Response(serializer.data)
class SettingsProfile(APIView):#проверка по нику так ка нет id 
    def get(self, request):
        data_list = Users.objects.all()
        serializer = UserModelSerializer(data_list, many=True)
        return Response(serializer.data)
    
    def put(self, request):
        username = request.data.get('username')
        try:
            user_profile = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_102_PROCESSING)
        
        serializer = UserModelSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView): 
    def get(self, request):
        data_list = Users.objects.all()
        serializer = UserModelSerializer(data_list, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate_user(username, password)
        if user:
            serializer = UserModelSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def authenticate_user(username_check, password):
    try:
        user = Users.objects.get(username=username_check)
        if user.password == password:
            return user
    except Users.DoesNotExist:
        pass
    return None

class RegistrationAPIView(APIView): 
    def post(self, request):
        data = request.data
        data['age'] = self.calculate_age(data.get('birthdate'))
        serializer = UserModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def calculate_age(self, birthdate):
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
    
class CheckEmailAPIView(APIView):
    def post(self, request):
        emailCheck = request.data.get('email')
        if Users.objects.filter(email=emailCheck).exists():
            return Response(True)
        else: return Response(False)

class CheckUsernameAPIView(APIView):
    def post(self, request):
        usernameCheck = request.data.get('username')
        if Users.objects.filter(username=usernameCheck).exists():
            return Response(True)
        else: return Response(False)

class AnimeListAPIView(APIView):
    def post(self, request):
        auth_code = request.data.get('codeInUrl')
        print("Received authorization code:", auth_code)  # Выводим значение auth_code в консоль
        if not auth_code:
            return Response({"message": "Authorization code is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        client_id = "krfXoP58e9I2LpvUArHfdmkx1yUrBjgpoPbQTut0hDI"
        client_secret = "JesmUCRQb2bBJY8cx-DMJcZych6NIJ2kv3jHbTXWBLg"
        redirect_uri = "http://localhost:3000/profile"
        
        access_token = get_access_token(client_id, client_secret, auth_code, redirect_uri)
        
        if not access_token:
            return Response({"message": "Failed to get access token"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        anime_titles = get_user_anime_ratings(access_token)
        
        if anime_titles is not None:
            return Response({"anime_titles": anime_titles}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Failed to get anime list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # Функция для получения id пользователя
def get_user_id(access_token):
    headers = {
        'User-Agent': 'MangaRecommendation',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://shikimori.one/api/users/whoami', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        return user_data['id']
    else:
        print(f'Failed to get user ID. Status code: {response.status_code}')
        return None
    
    # Функция для получения списка оцененных аниме пользователя с нормальными названиями
def get_user_anime_ratings(access_token):
    user_id = get_user_id(access_token)
    if user_id is not None:
        headers = {
            'User-Agent': 'MangaRecommendation',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(f'https://shikimori.one/api/v2/user_rates?user_id={user_id}', headers=headers)
        if response.status_code == 200:
            anime_ratings = response.json()
            anime_titles = []
            for rating in anime_ratings:
                anime_id = rating['target_id']
                anime_title = get_anime_title(anime_id, headers)
                anime_info = {
                    'title': anime_title,
                    'status': rating['status'],
                    'score': rating['score']
                }
                anime_titles.append(anime_info)
            return anime_titles
        else:
            print(f'Failed to get anime ratings. Status code: {response.status_code}')
            return None
    else:
        return None
    
    # Функция для получения названия аниме по его id
def get_anime_title(anime_id, headers):
    response = requests.get(f'https://shikimori.one/api/animes/{anime_id}', headers=headers)
    if response.status_code == 200:
        anime_data = response.json()
        return anime_data['russian']  # Здесь можно выбрать русское или английское название
    elif response.status_code == 429:
        print('Слишком много запросов. Ждем 15 секунд...')
        time.sleep(15)  # Добавляем задержку в 15 секунд
        return get_anime_title(anime_id, headers)  # Повторяем запрос
    else:
        print(f'Не удалось получить аниме. Код статуса: {response.status_code}')
        return None
    
    # Функция для получения access_token через процедуру аутентификации OAuth2
def get_access_token(client_id, client_secret, code, redirect_uri):
    headers = {
        'User-Agent': 'MangaRecommendation',
    }
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    }
    response = requests.post('https://shikimori.one/oauth/token', headers=headers, data=data)
    if response.status_code == 200:
        access_token_data = response.json()
        return access_token_data.get('access_token')
    else:
        print(f'Failed to get access token. Status code: {response.status_code}')
        return None
