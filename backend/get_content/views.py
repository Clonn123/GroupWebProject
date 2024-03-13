from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Animes, Anime_info
from .models import Users, Score
from .models import UserProfile
from .serializer import MyModelSerializer, InfoAnimeSerializer
from .serializer import UserModelSerializer, ScoreSerializer
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.decorators import api_view
from datetime import datetime
from django.db.models import Q
import requests
import time
import sqlite3
import re
from bs4 import BeautifulSoup
from django.db.models import Avg
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
class MyList(APIView): 
    def get(self, request, id, sort):
        # Получаем все записи из модели Score для указанного user_id
        score_records = Score.objects.filter(user_id=id)
        
        # Получаем все anime_id и score из этих записей
        anime_score_data = score_records.values_list('anime_id', 'score')
        
        # Извлекаем все anime_id и score из кортежей
        anime_ids, scores = zip(*anime_score_data)
        
        # Получаем все записи из модели Animes, связанные с этими anime_id
        data_list = Animes.objects.filter(anime_list_id__in=anime_ids).order_by(sort)
        
        # Создаем список словарей с атрибутами anime_id, score и другими данными из модели Animes
        serialized_data = []
        for anime in data_list:
            serialized_data.append({
                'anime_list_id': anime.anime_list_id,
                'url_img': anime.url_img,
                'descriptionData': anime.descriptionData,
                'descriptionEpisod': anime.descriptionEpisod,
                'title_ru': anime.title_ru, 
                'score': scores[anime_ids.index(anime.anime_list_id)] 
            })
        
        if sort == '-score' or sort == 'score':
            serialized_data = [item for item in serialized_data if item['score'] is not None]
            serialized_data.sort(key=lambda x: x['score'], reverse=(sort == '-score'))
        
        return Response(serialized_data)   
    
class InfoAPIView(APIView): 
    def get(self, request):
        id_anime = request.GET.get('id_anime')
        id_user = request.GET.get('id_user')
        try:
            anime_info = Anime_info.objects.get(anime_id=id_anime)
            serializer = InfoAnimeSerializer(anime_info)
            
            anime_info2 = Animes.objects.get(anime_list_id=id_anime)
            serializer2 = MyModelSerializer(anime_info2)
            
            try:
                anime_info3 = Score.objects.get(anime_id=id_anime, user_id=id_user)
                serializer3 = ScoreSerializer(anime_info3)
                
                scores_for_anime = Score.objects.filter(anime_id=id_anime)
                scores = scores_for_anime.values_list('score', flat=True)
                average_score = scores.aggregate(avg_score=Avg('score'))['avg_score']
                
                response_data = {
                "anime_info": serializer.data,
                "anime_info2": serializer2.data,
                "anime_info3": serializer3.data,
                "score": average_score
            }
            except:
                response_data = {
                "anime_info": serializer.data,
                "anime_info2": serializer2.data,
                "anime_info3": False,
                "score": 0
            }
            
            return Response(response_data)
        except Anime_info.DoesNotExist or Animes.DoesNotExist:
            return Response({"message": "Anime not found"}, status=status.HTTP_404_NOT_FOUND)
class IsWatched(APIView): 
    def get(self, request):
        id_user = request.GET.get('id_user')
        id_anime = request.GET.get('id_anime')
        try:
            score_table = Score.objects.get(anime_id=id_anime, user_id=id_user)
            if score_table.status == "completed":
                return Response("completed")
            elif score_table.status == "planned":
                return Response("planned")
            elif score_table.status == "dropped":
                return Response("dropped")
            elif score_table.status == "watching":
                return Response("watching")
            
        except Score.DoesNotExist:
            return Response(False)
        


class SearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        results = Animes.objects.filter(Q(title_en__startswith=query))
        serializer = MyModelSerializer(results, many=True)
        return Response(serializer.data)
    
class ScoreAPIView(APIView):
    def put(self, request):
        anime_id = request.data.get('anime_id')
        user_id = request.data.get('user_id')
        try:
            score_table = Score.objects.get(anime_id=anime_id, user_id=user_id)
            data = request.data
            serializer = ScoreSerializer(score_table, data=data, partial=True)
        except:
            data = request.data
            serializer = ScoreSerializer(data=data, partial=True)
            
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
        serializer = UserModelSerializer(data=data, partial=True)
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
        userId = request.data.get('userId')
        
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
        # запись твоих оценок жи есть
        for item in anime_titles:
            write_score_to_database(userId, item)
        remove_duplicate_scores(userId)
        
        if anime_titles is not None:
            return Response({"anime_titles": anime_titles}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Failed to get anime list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def isTable(anime_id):
    connection = sqlite3.connect('./db.sqlite3')
    cursor = connection.cursor()

    sql_query = "SELECT * FROM animes WHERE anime_list_id = ?"
    cursor.execute(sql_query, (anime_id,))

    anime_exists = cursor.fetchone() is not None

    connection.close()

    return not anime_exists

def writheBD(title_en, title_ru, url_img, descriptionEpisod, descriptionData, anime_list_id, score):
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO animes (anime_list_id, title_en, title_ru, url_img, descriptionEpisod, descriptionData, "
        "score) VALUES ("
        "?, ?, ?, ?, ?, ?, ?)",
        (anime_list_id, title_en, title_ru, url_img,
         descriptionEpisod, descriptionData, score))

    conn.commit()
    conn.close()

def writheInfo(anime_id, Episodes, Genres, Themes):
    connection = sqlite3.connect('./db.sqlite3')
    cursor = connection.cursor()

    sql_query = "INSERT INTO anime_info (anime_id, Episodes, Genres, Themes) " \
                "VALUES (?, ?, ?, ?)"
    cursor.execute(sql_query, (anime_id, Episodes, Genres, Themes))

    connection.commit()
    connection.close()

def find_missing_anime_list_ids():
    connection = sqlite3.connect('./db.sqlite3')
    cursor = connection.cursor()

    sql_query = """
        SELECT ti.title_id
        FROM temporary_info ti
        LEFT JOIN animes a ON ti.title_id = a.anime_list_id
        WHERE a.anime_list_id IS NULL
    """
    cursor.execute(sql_query)

    missing_anime_list_ids = [row[0] for row in cursor.fetchall()]

    connection.close()

    return missing_anime_list_ids

def scrapingShiki(anime_id):
    url = f'https://shikimori.one/animes/y{anime_id}'

    headers = {
        'User-Agent': 'AnimeRecommended'
    }
    response = requests.get(url, headers=headers)
    print(response)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        entry_info = soup.findAll('div', class_='line-container')

        try:
            episodes_container, genres_container, themes_container = None, None, None
            for container in entry_info:
                key_element = container.find('div', class_='key')
                key_text = key_element.text.strip()
                if key_text == 'Статус:':
                    status = container.find('div', class_='value')
                if key_text == 'Эпизоды:':
                    episodes_container = container.find('div', class_='value')
                if key_text == 'Жанры:' or key_text == 'Жанр:':
                    genres_container = container.find('div', class_='value')
                if key_text == 'Темы:' or key_text == 'Тема:':
                    themes_container = container.find('div', class_='value')

            print(anime_id)
            name = soup.find('header', class_='head')
            russian_title = soup.find('h1').contents[0]
            english_title = name.find('meta', {'itemprop': 'name'})['content']
            print(russian_title)
            print(english_title)

            Type = soup.find('div', class_='b-entry-info').contents[0]
            type_element = Type.find('div', class_='value')
            type_value = type_element.get_text(strip=True)
            print(type_value)

            img = soup.findAll('div', class_='c-poster')
            for i in img:
                meta_tag = i.find('meta', {'itemprop': 'image'})
                content_value = meta_tag['content']
            print(content_value)

            pattern = r'\b\d{4}\b'
            match = re.search(pattern, str(status)).group()
            print(match)

            score = soup.find('div', class_='c-info-right').find('meta', {'itemprop': 'ratingValue'})['content']
            print(score)

            try:
                episodes = episodes_container.text.strip().split("/")[-1].strip()
            except:
                episodes = 1
            print("Количество эпизодов:", episodes)

            genre_elements = genres_container.find_all('span', class_='genre-ru')
            genres = ', '.join([genre.text.strip() for genre in genre_elements])
            print("Жанры:", genres)

            try:
                themes_elements = themes_container.find_all('span', class_='genre-ru')
                themes = ', '.join([themes.text.strip() for themes in themes_elements])
            except:
                themes = None
            print("Темы:", themes)

            prov = isTable(anime_id)
            if prov:
                writheBD(english_title, russian_title, content_value, type_value, match, anime_id, score)
                writheInfo(anime_id, episodes, genres, themes)
                print(prov)
            else:
                print(prov)

            print("--------")
        except:
            return
    
            
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
    
def writheTemporaryInfo(title_id, title, status, score):
    connection = sqlite3.connect('./db.sqlite3')
    cursor = connection.cursor()

    sql_query = "INSERT INTO temporary_info (title_id, title, status, score) " \
                "VALUES (?, ?, ?, ?)"
    cursor.execute(sql_query, (title_id, title, status, score))

    connection.commit()
    connection.close()
    
def clearTemporaryInfo():
    connection = sqlite3.connect('./db.sqlite3')
    cursor = connection.cursor()

    sql_query = "DELETE FROM temporary_info"
    cursor.execute(sql_query)

    connection.commit()
    connection.close()
     
    # Функция для получения списка оцененных аниме пользователя с нормальными названиями

def write_score_to_database(user_id, anime_info):
    try:
        score = Score(
            user_id=user_id,
            anime_id=anime_info['title_id'],
            status=anime_info['status'],
            score=anime_info['score']
        )
        
        score.save()
        
        return True  
    except Exception as e:
        print("Ошибка при записи в базу данных:", e)
        return False  
def remove_duplicate_scores(user_id):
    # Получаем список уникальных anime_id для заданного user_id
    unique_anime_ids = Score.objects.filter(user_id=user_id).values_list('anime_id', flat=True).distinct()

    # Удаляем записи с повторяющимися anime_id
    Score.objects.filter(user_id=user_id).exclude(anime_id__in=unique_anime_ids).delete()
    
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
            clearTemporaryInfo()
            for rating in anime_ratings:
                if rating['target_type'] == "Anime": 
                    anime_id = rating['target_id']
                    anime_title = get_anime_title(anime_id, headers)
                    anime_info = {
                        'title_id': rating['target_id'],
                        'title': anime_title,
                        'status': rating['status'],
                        'score': rating['score']
                    }
                    writheTemporaryInfo(anime_info['title_id'], anime_info['title'],
                               anime_info['status'], anime_info['score'])    
                    anime_titles.append(anime_info)
                # if rating['target_type'] == "Manga":
            not_bd_id = find_missing_anime_list_ids()
            print(not_bd_id)
            for item in not_bd_id:
                scrapingShiki(item) 
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
        print('Слишком много запросов. Ждем 10 секунд...')
        time.sleep(10)  # Добавляем задержку в 10 секунд
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

#гордо рекомендации

def Recommendations_SVD():
    pass
    
