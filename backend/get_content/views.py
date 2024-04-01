from random import Random
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Animes, Anime_info
from .models import Mangas, Manga_info
from .models import Users, Score
from .models import UserProfile
from .serializer import MyModelSerializer, InfoAnimeSerializer
from .serializer import MangaSerializer, InfoMangaSerializer, Score_manga
from .serializer import UserModelSerializer, ScoreSerializer, ScoreMangaSerializer
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.decorators import api_view
from datetime import datetime
from django.db.models import Q
import requests
import time
import sqlite3
import re
from urllib.parse import unquote
from bs4 import BeautifulSoup
from django.db.models import Avg
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from django.core.paginator import Paginator
from urllib.parse import urlparse, parse_qs
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from random import shuffle
from sklearn.feature_extraction.text import CountVectorizer

class DataAPIView(APIView): 
    def get(self, request, sort):
        if (sort == '-score' or sort == '-descriptionData' or sort == '-title_ru'
            or sort == 'score' or sort == 'descriptionData' or sort == 'title_ru'):
            data_list = Animes.objects.order_by(f'{sort}')
        else:
            data_list = Animes.objects.all()
            
        paginator = Paginator(data_list, 20)  # Разбиваем данные на страницы, по 20 элементов на каждой
        page_number = request.GET.get('pageNumber')  # Получаем номер страницы из запроса
        page_obj = paginator.get_page(page_number)  # Получаем объект страницы
        print(page_number)
    
        serializer = MyModelSerializer(page_obj, many=True)
        
        totalCount = int(data_list.count()/20)+1
        response_data = {
            'total_elements': totalCount,
            'data': serializer.data
        }
        return Response(response_data)
    
class DataMangaAPIView(APIView): 
    def get(self, request, sort):
        if (sort == '-score' or sort == '-descriptionData' or sort == '-title_ru'
            or sort == 'score' or sort == 'descriptionData' or sort == 'title_ru'):
            data_list = Mangas.objects.order_by(f'{sort}')
        else:
            data_list = Mangas.objects.all()
            
        paginator = Paginator(data_list, 20)  # Разбиваем данные на страницы, по 20 элементов на каждой
        page_number = request.GET.get('pageNumber')  # Получаем номер страницы из запроса
        page_obj = paginator.get_page(page_number)  # Получаем объект страницы
        print(page_number)
    
        serializer = MangaSerializer(page_obj, many=True)
        
        totalCount = int(data_list.count()/20)+1
        response_data = {
            'total_elements': totalCount,
            'data': serializer.data
        }
        return Response(response_data)
    
class MyList(APIView): 
    def get(self, request, id, sort):
        score_records = Score.objects.filter(user_id=id)
        anime_score_data = score_records.values_list('anime_id', 'score')
        anime_ids, scores = zip(*anime_score_data)
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

class MyListManga(APIView): 
    def get(self, request, id, sort):
        score_records = Score_manga.objects.filter(user_id=id)
        manga_score_data = score_records.values_list('manga_id', 'score')
        manga_ids, scores = zip(*manga_score_data)
        data_list = Mangas.objects.filter(manga_list_id__in=manga_ids).order_by(sort)
        
        serialized_data = []
        for manga in data_list:
            serialized_data.append({
                'manga_list_id': manga.manga_list_id,
                'url_img': manga.url_img,
                'descriptionData': manga.descriptionData,
                'descriptionEpisod': manga.descriptionEpisod,
                'title_ru': manga.title_ru, 
                'score': scores[manga_ids.index(manga.manga_list_id)] 
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
        
class InfoMangaAPIView(APIView): 
    def get(self, request):
        id_manga = request.GET.get('id_manga')
        id_user = request.GET.get('id_user')
        try:
            manga_info = Manga_info.objects.get(manga_id=id_manga)
            serializer = InfoMangaSerializer(manga_info)
            
            manga_info2 = Mangas.objects.get(manga_list_id=id_manga)
            serializer2 = MangaSerializer(manga_info2)
            
            try:
                manga_info3 = Score_manga.objects.get(manga_id=id_manga, user_id=id_user)
                serializer3 = ScoreMangaSerializer(manga_info3)
                
                scores_for_manga = Score_manga.objects.filter(manga_id=id_manga)
                scores = scores_for_manga.values_list('score', flat=True)
                average_score = scores.aggregate(avg_score=Avg('score'))['avg_score']
                
                response_data = {
                "manga_info": serializer.data,
                "manga_info2": serializer2.data,
                "manga_info3": serializer3.data,
                "score": average_score
            }
            except:
                response_data = {
                "manga_info": serializer.data,
                "manga_info2": serializer2.data,
                "manga_info3": False,
                "score": 0
            }
            
            return Response(response_data)
        except Manga_info.DoesNotExist or Mangas.DoesNotExist:
            return Response({"message": "Manga not found"}, status=status.HTTP_404_NOT_FOUND)

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

class IsWatchedManga(APIView): 
    def get(self, request):
        id_user = request.GET.get('id_user')
        id_manga = request.GET.get('id_manga')
        try:
            score_table = Score_manga.objects.get(manga_id=id_manga, user_id=id_user)
            if score_table.status == "completed":
                return Response("completed")
            elif score_table.status == "planned":
                return Response("planned")
            elif score_table.status == "dropped":
                return Response("dropped")
            elif score_table.status == "watching":
                return Response("watching")
            
        except Score_manga.DoesNotExist:
            return Response(False)        

class SearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        ru = unquote(query)
        Ru = ru.capitalize()
        results = Animes.objects.filter(
            Q(title_ru__icontains=ru) | Q(title_en__icontains=query)
            | Q(title_ru__icontains=Ru))
        serializer = MyModelSerializer(results, many=True)
        return Response(serializer.data)

class SearchMangaAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        ru = unquote(query)
        Ru = ru.capitalize()
        results = Mangas.objects.filter(
            Q(title_ru__icontains=ru) | Q(title_en__icontains=query)
            | Q(title_ru__icontains=Ru))
        serializer = MangaSerializer(results, many=True)
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
    
class ScoreMangaAPIView(APIView):
    def put(self, request):
        manga_id = request.data.get('manga_id')
        user_id = request.data.get('user_id')
        try:
            score_table = Score_manga.objects.get(manga_id=manga_id, user_id=user_id)
            data = request.data
            serializer = ScoreMangaSerializer(score_table, data=data, partial=True)
        except:
            data = request.data
            serializer = ScoreMangaSerializer(data=data, partial=True)
            
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DelObject(APIView):
    def post(self, request):
        anime_id = request.data.get('anime_id')
        user_id = request.data.get('user_id')
        score_table = Score.objects.get(anime_id=anime_id, user_id=user_id)
        score_table.delete()
        return Response({'message': 'Объект успешно удален из списка'})

class DelMangaObject(APIView):
    def post(self, request):
        manga_id = request.data.get('manga_id')
        user_id = request.data.get('user_id')
        score_table = Score_manga.objects.get(manga_id=manga_id, user_id=user_id)
        score_table.delete()
        return Response({'message': 'Объект успешно удален из списка'})     
    
class SettingsProfile(APIView):
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
            # Генерируем access токен для пользователя
            access_token = AccessToken.for_user(user)
            # Добавляем идентификатор пользователя в токен
            access_token['user_id'] = user.id
             # Сериализуем токен
            # token_serializer = TokenObtainPairSerializer(access_token)

            # Возвращаем access токен и данные пользователя
            return Response({
                'access_token': str(access_token),
                # 'refresh_token': token_serializer.data
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def authenticate_user(username_check, password):
    try:
        user = Users.objects.get(username=username_check)
        if check_password(password, user.password):
            return user
    except Users.DoesNotExist:
        pass
    return None

class UserAPIView(APIView):
    def get(self, request, user_id):
        get_id = user_id
        try:
            user_profile = Users.objects.get(id=get_id)
            serializer = UserModelSerializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

class RegistrationAPIView(APIView): 
    def post(self, request):
        data = request.data

        # Проверяем уникальность имени пользователя и адреса электронной почты
        username = data['username']
        email = data['email']
        if Users.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_401_UNAUTHORIZED)
        if Users.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Хешируем пароль
        data['password'] = make_password(data['password'])

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
        
        
        for item in anime_titles:
            write_score_to_database(userId, item)
        remove_duplicate_scores()

        manga_titles = get_user_manga_ratings(access_token)
        
        for item in manga_titles:
            write_score_manga_to_database(userId, item)
        remove_duplicate_scores_manga()
        
        if manga_titles is not None:
            return Response({"manga_titles": manga_titles}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Failed to get anime list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class MangaListAPIView(APIView):
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
        
        manga_titles = get_user_manga_ratings(access_token)
        
        # запись твоих оценок жи есть
        for item in manga_titles:
            write_score_manga_to_database(userId, item)
        remove_duplicate_scores_manga()
        
        if manga_titles is not None:
            return Response({"manga_titles": manga_titles}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Failed to get manga list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def isTable(anime_id):
    connection = sqlite3.connect('./db.sqlite3')
    cursor = connection.cursor()

    sql_query = "SELECT * FROM animes WHERE anime_list_id = ?"
    cursor.execute(sql_query, (anime_id,))

    anime_exists = cursor.fetchone() is not None

    connection.close()

    return not anime_exists

def isTableManga(manga_id):
    connection = sqlite3.connect('./db.sqlite3')
    cursor = connection.cursor()

    sql_query = "SELECT * FROM mangas WHERE manga_list_id = ?"
    cursor.execute(sql_query, (manga_id,))

    manga_exists = cursor.fetchone() is not None

    connection.close()

    return not manga_exists

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

def writeMangaBD(title_en, title_ru, url_img, descriptionEpisod, descriptionData, manga_list_id, score):
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO mangas (manga_list_id, title_en, title_ru, url_img, descriptionEpisod, descriptionData, "
        "score) VALUES ("
        "?, ?, ?, ?, ?, ?, ?)",
        (manga_list_id, title_en, title_ru, url_img,
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

def writeMangaInfo(manga_id, Episodes, Genres, Themes):
    connection = sqlite3.connect('./db.sqlite3')
    cursor = connection.cursor()

    sql_query = "INSERT INTO manga_info (manga_id, Episodes, Genres, Themes) " \
                "VALUES (?, ?, ?, ?)"
    cursor.execute(sql_query, (manga_id, Episodes, Genres, Themes))

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

def find_missing_manga_list_ids():
    connection = sqlite3.connect('./db.sqlite3')
    cursor = connection.cursor()

    sql_query = """
        SELECT ti.title_id
        FROM temporary_info_manga ti
        LEFT JOIN mangas a ON ti.title_id = a.manga_list_id
        WHERE a.manga_list_id IS NULL
    """
    cursor.execute(sql_query)

    missing_manga_list_ids = [row[0] for row in cursor.fetchall()]

    connection.close()

    return missing_manga_list_ids

def write_studio_to_db(anime_list_id, studio):
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE animes SET studios = ? WHERE anime_list_id = ?",
        (studio, anime_list_id)
    )
    conn.commit()
    conn.close()

def write_authors_to_db(manga_list_id, studio):
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE mangas SET authors = ? WHERE manga_list_id = ?",
        (studio, manga_list_id)
    )
    conn.commit()
    conn.close()
    
def scrape_studio(id):
    url = f'https://myanimelist.net/anime/{id}'

    response = requests.get(url)
    if response.status_code != 200:
        time.sleep(10)
        
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        studio_elements = soup.find_all('div', class_='spaceit_pad')

        studio_name = ''
        for studio_element in studio_elements:
            text = studio_element.get_text()
            if 'Studios:' in text:
                studio_name = studio_element.find('a').get_text()
                print(studio_name)

        if studio_name == '':
            write_studio_to_db(id, "нет")
        else:
            write_studio_to_db(id, studio_name)

def scrape_authors(id):
    url = f'https://myanimelist.net/manga/{id}'

    response = requests.get(url)
    if response.status_code != 200:
        time.sleep(10)
        
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        authors_elements = soup.find_all('div', class_='spaceit_pad')

        authors_name = ''
        for authors_element in authors_elements:
            text = authors_element.get_text()
            if 'Authors:' in text:
                authors_name = authors_element.find('a').get_text()
                print(authors_name)

        if authors_name == '':
            write_authors_to_db(id, "нет")
        else:
            write_authors_to_db(id, authors_name)

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
                scrape_studio(anime_id)
                print(prov)
            else:
                print(prov)

            print("--------")
        except:
            return

def scrapingShikiManga(manga_id):
    url = f'https://shikimori.one/mangas/{manga_id}'

    headers = {
        'User-Agent': 'MangaRecommendation'
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
                if key_text == 'Главы:':
                    episodes_container = container.find('div', class_='value')
                if key_text == 'Жанры:' or key_text == 'Жанр:':
                    genres_container = container.find('div', class_='value')
                if key_text == 'Темы:' or key_text == 'Тема:':
                    themes_container = container.find('div', class_='value')

            print(manga_id)
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
            print("Количество глав:", episodes)

            genre_elements = genres_container.find_all('span', class_='genre-ru')
            genres = ', '.join([genre.text.strip() for genre in genre_elements])
            print("Жанры:", genres)

            try:
                themes_elements = themes_container.find_all('span', class_='genre-ru')
                themes = ', '.join([themes.text.strip() for themes in themes_elements])
            except:
                themes = None
            print("Темы:", themes)

            prov = isTableManga(manga_id)
            if prov:
                writeMangaBD(english_title, russian_title, content_value, type_value, match, manga_id, score)
                writeMangaInfo(manga_id, episodes, genres, themes)
                scrape_authors(manga_id)
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

def writheTemporaryInfoManga(title_id, title, status, score):
    connection = sqlite3.connect('./db.sqlite3')
    cursor = connection.cursor()

    sql_query = "INSERT INTO temporary_info_manga (title_id, title, status, score) " \
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
     
def clearTemporaryInfoManga():
    connection = sqlite3.connect('./db.sqlite3')
    cursor = connection.cursor()

    sql_query = "DELETE FROM temporary_info_manga"
    cursor.execute(sql_query)

    connection.commit()
    connection.close()

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
    
def write_score_manga_to_database(user_id, manga_info):
    try:
        score = Score_manga(
            user_id=user_id,
            manga_id=manga_info['title_id'],
            status=manga_info['status'],
            score=manga_info['score']
        )
        
        score.save()
        
        return True  
    except Exception as e:
        print("Ошибка при записи в базу данных:", e)
        return False  

def remove_duplicate_scores():
    connection = sqlite3.connect('./db.sqlite3')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM score WHERE rowid NOT IN (SELECT MIN(rowid) FROM score GROUP BY user_id, anime_id)')

    connection.commit()
    connection.close()

def remove_duplicate_scores_manga():
    connection = sqlite3.connect('./db.sqlite3')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM score_manga WHERE rowid NOT IN (SELECT MIN(rowid) FROM score_manga GROUP BY user_id, manga_id)')

    connection.commit()
    connection.close()
    
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

def get_user_manga_ratings(access_token):
    user_id = get_user_id(access_token)
    if user_id is not None:
        headers = {
            'User-Agent': 'MangaRecommendation',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(f'https://shikimori.one/api/v2/user_rates?user_id={user_id}', headers=headers)
        if response.status_code == 200:
            anime_ratings = response.json()
            manga_titles = []
            clearTemporaryInfoManga()
            for rating in anime_ratings:
                if rating['target_type'] == "Manga": 
                    manga_id = rating['target_id']
                    manga_title = get_manga_title(manga_id, headers)
                    manga_info = {
                        'title_id': rating['target_id'],
                        'title': manga_title,
                        'status': rating['status'],
                        'score': rating['score']
                    }
                    writheTemporaryInfoManga(manga_info['title_id'], manga_info['title'],
                               manga_info['status'], manga_info['score'])    
                    manga_titles.append(manga_info)
            not_bd_id = find_missing_manga_list_ids()
            print(not_bd_id)
            for item in not_bd_id:
                scrapingShikiManga(item) 
            return manga_titles
        else:
            print(f'Failed to get manga ratings. Status code: {response.status_code}')
            return None
    else:
        return None

def get_anime_title(anime_id, headers):
    response = requests.get(f'https://shikimori.one/api/animes/{anime_id}', headers=headers)
    if response.status_code == 200:
        anime_data = response.json()
        return anime_data['russian']  # Здесь можно выбрать русское или английское название
    elif response.status_code == 429:
        print('Слишком много запросов к аниме. Ждем 10 секунд...')
        time.sleep(10)  # Добавляем задержку в 10 секунд
        return get_anime_title(anime_id, headers)  # Повторяем запрос
    else:
        print(f'Не удалось получить аниме. Код статуса: {response.status_code}')
        return None
    
    # Функция для получения access_token через процедуру аутентификации OAuth2

def get_manga_title(manga_id, headers):
    response = requests.get(f'https://shikimori.one/api/mangas/{manga_id}', headers=headers)
    if response.status_code == 200:
        mangas_data = response.json()
        return mangas_data['russian']
    elif response.status_code == 429:
        print('Слишком много запросов к манге. Ждем 10 секунд...')
        time.sleep(10)  # Добавляем задержку в 10 секунд
        return get_manga_title(manga_id, headers)  # Повторяем запрос
    else:
        print(f'Не удалось получить манги. Код статуса: {response.status_code}')
        return None

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

def convert_to_ssv(data):
        ssv_data = []
        for item in data:
            ssv_item = ' '.join(str(value) for value in item.values())
            ssv_data.append(ssv_item)
        return '\n'.join(ssv_data)
    
def save_ssv_file(data, filename):
    # Создаем строку с заголовками столбцов
    header = 'anime_id, type, data, score_real, episodes, Genres, Themes\n'
    
    with open(filename, 'w') as file:
        # Записываем заголовок в файл
        file.write(header)
        
        # Записываем данные в файл
        for item in data:
            # Вставляем объединенную строку вместо Genres и Themes
            genres_themes = f"{item.get('Genres', ' ')} {item.get('Themes', ' ')}"
            ssv_item = ', '.join([
                str(item.get('anime_id', '')),
                str(item.get('type', '')),
                str(item.get('data', '')),
                str(item.get('score_real', '')),
                str(item.get('episodes', '')),
                genres_themes
            ])
            file.write(ssv_item + '\n')

def save_ssv_file_manga(data, filename):
    # Создаем строку с заголовками столбцов
    header = 'manga_id, type, data, score_real, episodes, Genres, Themes\n'
    
    with open(filename, 'w') as file:
        # Записываем заголовок в файл
        file.write(header)
        
        # Записываем данные в файл
        for item in data:
            # Вставляем объединенную строку вместо Genres и Themes
            genres_themes = f"{item.get('Genres', ' ')} {item.get('Themes', ' ')}"
            ssv_item = ', '.join([
                str(item.get('manga_id', '')),
                str(item.get('type', '')),
                str(item.get('data', '')),
                str(item.get('score_real', '')),
                str(item.get('episodes', '')),
                genres_themes
            ])
            file.write(ssv_item + '\n')

#гордо рекомендации
def get_info_user(id_user):
    scores = Score.objects.filter(user_id=id_user)
    serializer = ScoreSerializer(scores, many=True)
    
    anime_ids = [score.anime_id for score in scores]
    all_info = Animes.objects.filter(anime_list_id__in=anime_ids)
    serializer2 = MyModelSerializer(all_info, many=True)
    
    anime_info = Anime_info.objects.filter(anime_id__in=anime_ids)
    serializer3 = InfoAnimeSerializer(anime_info, many=True)
    
    data_dict = {}
    
    for i, score_data in enumerate(serializer.data):
        anime_id = score_data['anime_id']
        if anime_id not in data_dict:
            data_dict[anime_id] = {
                'anime_id': anime_id,
                'type': None,
                'data': None,
                'score_user': None,
                'score_real': None,
                'episodes': None,
                'studios': None,
                'Genres': None,
                'Themes': None,
            }
        data_dict[anime_id]['score_user'] = score_data['score']
    
    for i, anime_data in enumerate(serializer2.data):
        anime_id = anime_data['anime_list_id']
        if anime_id not in data_dict:
            data_dict[anime_id] = {
                'anime_id': anime_id,
                'type': None,
                'data': None,
                'score_user': None,
                'score_real': None,
                'episodes': None,
                'studios': None,
                'Genres': None,
                'Themes': None,
            }
        data_dict[anime_id]['type'] = anime_data['descriptionEpisod']
        data_dict[anime_id]['data'] = anime_data['descriptionData']
        data_dict[anime_id]['score_real'] = anime_data['score']
    
    for i, info_data in enumerate(serializer3.data):
        anime_id = info_data['anime_id']
        if anime_id not in data_dict:
            data_dict[anime_id] = {
                'anime_id': anime_id,
                'type': None,
                'data': None,
                'score_user': None,
                'score_real': None,
                'episodes': None,
                'studios': None,
                'Genres': None,
                'Themes': None,
            }
        data_dict[anime_id]['episodes'] = info_data['Episodes']
        data_dict[anime_id]['Genres'] = info_data['Genres']
        data_dict[anime_id]['Themes'] = info_data['Themes']
    
    data = list(data_dict.values())
    ssv_data = convert_to_ssv(data)
    
    return [data, ssv_data, anime_ids]

def get_info_user_manga(id_user):
    scores = Score_manga.objects.filter(user_id=id_user)
    serializer = ScoreMangaSerializer(scores, many=True)
    
    manga_ids = [score.manga_id for score in scores]
    all_info = Mangas.objects.filter(manga_list_id__in=manga_ids)
    serializer2 = MangaSerializer(all_info, many=True)
    
    manga_info = Manga_info.objects.filter(manga_id__in=manga_ids)
    serializer3 = InfoMangaSerializer(manga_info, many=True)
    
    data_dict = {}
    
    for i, score_data in enumerate(serializer.data):
        manga_id = score_data['manga_id']
        if manga_id not in data_dict:
            data_dict[manga_id] = {
                'manga_id': manga_id,
                'type': None,
                'data': None,
                'score_user': None,
                'score_real': None,
                'episodes': None,
                'authors': None,
                'Genres': None,
                'Themes': None,
            }
        data_dict[manga_id]['score_user'] = score_data['score']
    
    for i, manga_data in enumerate(serializer2.data):
        manga_id = manga_data['manga_list_id']
        if manga_id not in data_dict:
            data_dict[manga_id] = {
                'manga_id': manga_id,
                'type': None,
                'data': None,
                'score_user': None,
                'score_real': None,
                'episodes': None,
                'authors': None,
                'Genres': None,
                'Themes': None,
            }
        data_dict[manga_id]['type'] = manga_data['descriptionEpisod']
        data_dict[manga_id]['data'] = manga_data['descriptionData']
        data_dict[manga_id]['score_real'] = manga_data['score']
    
    for i, info_data in enumerate(serializer3.data):
        manga_id = info_data['manga_id']
        if manga_id not in data_dict:
            data_dict[manga_id] = {
                'manga_id': manga_id,
                'type': None,
                'data': None,
                'score_user': None,
                'score_real': None,
                'episodes': None,
                'authors': None,
                'Genres': None,
                'Themes': None,
            }
        data_dict[manga_id]['episodes'] = info_data['Episodes']
        data_dict[manga_id]['Genres'] = info_data['Genres']
        data_dict[manga_id]['Themes'] = info_data['Themes']
    
    data = list(data_dict.values())
    ssv_data = convert_to_ssv(data)
    
    return [data, ssv_data, manga_ids]

def get_full_info(anime_ids_to_exclude):
    full_info = []
    anime_list = Animes.objects.exclude(anime_list_id__in=anime_ids_to_exclude)
    for anime in anime_list:
        anime_serializer = MyModelSerializer(anime)
        info = Anime_info.objects.get(anime_id=anime.anime_list_id)
        info_serializer = InfoAnimeSerializer(info)
        full_info.append({
            'anime_id': anime_serializer.data['anime_list_id'],
            'type': anime_serializer.data['descriptionEpisod'],
            
            'title_ru': anime_serializer.data['title_ru'],
            'url_img': anime_serializer.data['url_img'],
            
            'data': anime_serializer.data['descriptionData'],
            'score_real': anime_serializer.data['score'],
            'studios': anime_serializer.data['studios'],
            
            'episodes': info_serializer.data['Episodes'],
            'Genres': info_serializer.data['Genres'],
            'Themes': info_serializer.data['Themes'],
        })
    
    ssv_data = convert_to_ssv(full_info)
    return [full_info, ssv_data]

def get_full_info_manga(manga_ids_to_exclude):
    full_info = []
    manga_list = Mangas.objects.exclude(manga_list_id__in=manga_ids_to_exclude)
    for manga in manga_list:
        manga_serializer = MangaSerializer(manga)
        info = Manga_info.objects.get(manga_id=manga.manga_list_id)
        info_serializer = InfoMangaSerializer(info)
        full_info.append({
            'manga_id': manga_serializer.data['manga_list_id'],
            'type': manga_serializer.data['descriptionEpisod'],
            
            'title_ru': manga_serializer.data['title_ru'],
            'url_img': manga_serializer.data['url_img'],
            
            'data': manga_serializer.data['descriptionData'],
            'score_real': manga_serializer.data['score'],
            'authors': manga_serializer.data['authors'],
            
            'episodes': info_serializer.data['Episodes'],
            'Genres': info_serializer.data['Genres'],
            'Themes': info_serializer.data['Themes'],
        })
    
    ssv_data = convert_to_ssv(full_info)
    return [full_info, ssv_data]

def content_based_filtering_sklearn(user_preferences, anime_data):
    vectorizer = TfidfVectorizer()
    
    anime_descriptions = [f"{anime['type']} {anime['data']} {anime['Genres']} {anime['Themes']} {anime['score_real']} {anime['studios']}" for anime in anime_data]
    user_preferences_descriptions = [f"{anime['type']} {anime['data']} {anime['Genres']} {anime['Themes']} {anime['score_user']} {anime['studios']}" for anime in user_preferences]
    
    # Создаем TF-IDF векторизаторизацию
    tfidf_matrix = vectorizer.fit_transform(anime_descriptions)
    user_preferences_tfidf = vectorizer.transform(user_preferences_descriptions)
    
    # Вычисляем косинусную близость между предпочтениями пользователя и характеристиками аниме
    cosine_similarities = cosine_similarity(user_preferences_tfidf, tfidf_matrix)

    # Умножаем косинусные близости на оценки пользователя (нихуя не делает)
    user_scores = np.array([anime['score_user'] for anime in user_preferences])
    user_scores = np.tile(user_scores.reshape(-1, 1), (1, cosine_similarities.shape[1]))
    weighted_cosine_similarities = cosine_similarities * user_scores

    # Получаем индексы аниме, наиболее близкие к предпочтениям пользователя
    similar_anime_indices = cosine_similarities.argsort()[0][::-1]
    recommendations = [anime_data[index] for index in similar_anime_indices]

    return recommendations

def content_based_filtering_sklearn_manga(user_preferences, manga_data):
    vectorizer = TfidfVectorizer()
    
    manga_descriptions = [f"{manga['type']} {manga['data']} {manga['Genres']} {manga['Themes']} {manga['score_real']} {manga['authors']}" for manga in manga_data]
    user_preferences_descriptions = [f"{manga['type']} {manga['data']} {manga['Genres']} {manga['Themes']} {manga['score_user']} {manga['authors']}" for manga in user_preferences]
    # Создаем TF-IDF векторизаторизацию
    tfidf_matrix = vectorizer.fit_transform(manga_descriptions)
    user_preferences_tfidf = vectorizer.transform(user_preferences_descriptions)
    
    # Вычисляем косинусную близость между предпочтениями пользователя и характеристиками аниме
    cosine_similarities = cosine_similarity(user_preferences_tfidf, tfidf_matrix)

    # Умножаем косинусные близости на оценки пользователя (нихуя не делает)
    user_scores = np.array([manga['score_user'] for manga in user_preferences])
    user_scores = np.tile(user_scores.reshape(-1, 1), (1, cosine_similarities.shape[1]))
    weighted_cosine_similarities = cosine_similarities * user_scores

    # Получаем индексы аниме, наиболее близкие к предпочтениям пользователя
    similar_manga_indices = cosine_similarities.argsort()[0][::-1]
    recommendations = [manga_data[index] for index in similar_manga_indices]

    return recommendations

def svd_based_filtering(user_preferences, anime_data):
    vectorizer = TfidfVectorizer()
    anime_descriptions = [f"{anime['type']} {anime['data']} {anime['Genres']} {anime['Themes']} {anime['score_real']} {anime['studios']}" for anime in anime_data]
    user_preferences_descriptions = [f"{anime['type']} {anime['data']} {anime['Genres']} {anime['Themes']} {anime['score_user']} {anime['studios']}" for anime in user_preferences]
    tfidf_matrix = vectorizer.fit_transform(anime_descriptions)
    user_preferences_tfidf = vectorizer.transform(user_preferences_descriptions)

    # Применяем метод SVD для сокращения размерности
    svd = TruncatedSVD(n_components=100)
    tfidf_svd = svd.fit_transform(tfidf_matrix)
    user_preferences_tfidf_svd = svd.transform(user_preferences_tfidf)

    # Вычисляем косинусную близость между предпочтениями пользователя и характеристиками аниме после сокращения размерности
    cosine_similarities_svd = cosine_similarity(user_preferences_tfidf_svd, tfidf_svd)

    # Получаем индексы аниме, наиболее близкие к предпочтениям пользователя
    similar_anime_indices = cosine_similarities_svd.argsort()[0][::-1]
    recommendations = [anime_data[index] for index in similar_anime_indices]

    return recommendations

def svd_based_filtering_manga(user_preferences, manga_data):
    vectorizer = CountVectorizer()
    manga_descriptions = [f"{manga['type']} {manga['data']} {manga['Genres']} {manga['Themes']} {manga['score_real']} {manga['authors']}" for manga in manga_data]
    user_preferences_descriptions = [f"{manga['type']} {manga['data']} {manga['Genres']} {manga['Themes']} {manga['score_user']} {manga['authors']}" for manga in user_preferences]
    tfidf_matrix = vectorizer.fit_transform(manga_descriptions)
    user_preferences_tfidf = vectorizer.transform(user_preferences_descriptions)

    svd = TruncatedSVD(n_components=100)
    tfidf_svd = svd.fit_transform(tfidf_matrix)
    user_preferences_tfidf_svd = svd.transform(user_preferences_tfidf)

    cosine_similarities_svd = cosine_similarity(user_preferences_tfidf_svd, tfidf_svd)

    similar_manga_indices = cosine_similarities_svd.argsort()[0][::-1]
    recommendations = [manga_data[index] for index in similar_manga_indices]

    return recommendations     

class Recommendations_CBF(APIView):
    def get(self, request):
        id_user = request.GET.get('id_user')
        page_number = request.GET.get('pageNumber')
        method = request.GET.get('method')
        print(f"method: {method}")
        
        count = Score.objects.filter(user_id=id_user)
        if len(count) < 20:
            return Response(False)
        
        
        user_info = get_info_user(id_user)
        user_info_list = user_info[0] 
        
        excluded_anime_ids = user_info[2] 
        full_info = get_full_info(excluded_anime_ids)
        full_info_list = full_info[0] 
        
        response_data = {
            'user_info_list': user_info_list,
            'full_info_list': full_info_list,
        } 
        
        if method == 'CBF':
            recommendations = content_based_filtering_sklearn(user_info_list, full_info_list)
            paginator = Paginator(recommendations, 20)
            page_obj = paginator.get_page(page_number)
             
        if method == 'SVD':
            recommendations = svd_based_filtering(user_info_list, full_info_list)
            paginator = Paginator(recommendations, 20)
            page_obj = paginator.get_page(page_number)
            
        
        serialized_data = []
        for recommendation in page_obj:
            recommendation_data = {
                "anime_id": recommendation.get("anime_id"),
                "type": recommendation.get("type"),
                "title_ru": recommendation.get("title_ru"),
                "url_img": recommendation.get("url_img"),
                "data": recommendation.get("data"),
                "score_real": recommendation.get("score_real"),
                "episodes": recommendation.get("episodes"),
                "Genres": recommendation.get("Genres"),
                "Themes": recommendation.get("Themes")
            }
            serialized_data.append(recommendation_data) 

        
        return Response(serialized_data)
        
class Recommendations_CBF_Manga(APIView):
    def get(self, request):
        id_user = request.GET.get('id_user')
        page_number = request.GET.get('pageNumber')
        method = request.GET.get('method')
        print(f"method: {method}")
        
        count = Score_manga.objects.filter(user_id=id_user)
        if len(count) < 20:
            return Response(False)
        
        user_info = get_info_user_manga(id_user)
        user_info_list = user_info[0] 
        
        excluded_manga_ids = user_info[2] 
        full_info = get_full_info_manga(excluded_manga_ids)
        full_info_list = full_info[0] 
        response_data = {
            'user_info_list': user_info_list,
            'full_info_list': full_info_list,
        } 
        if method == 'CBF':
            recommendationsCBF = content_based_filtering_sklearn_manga(user_info_list, full_info_list)
            paginator = Paginator(recommendationsCBF, 20)
            page_obj = paginator.get_page(page_number)
        if method == 'SVD':
            recommendationsSVD = svd_based_filtering_manga(user_info_list, full_info_list)
            paginator = Paginator(recommendationsSVD, 20)
            page_obj = paginator.get_page(page_number) 
        
        serialized_data = []
        for recommendation in page_obj:
            recommendation_data = {
                "manga_id": recommendation.get("manga_id"),
                "type": recommendation.get("type"),
                "title_ru": recommendation.get("title_ru"),
                "url_img": recommendation.get("url_img"),
                "data": recommendation.get("data"),
                "score_real": recommendation.get("score_real"),
                "episodes": recommendation.get("episodes"),
                "Genres": recommendation.get("Genres"),
                "Themes": recommendation.get("Themes")
            }
            serialized_data.append(recommendation_data) 

        
        return Response(serialized_data)