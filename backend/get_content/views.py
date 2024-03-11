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
                response_data = {
                "anime_info": serializer.data,
                "anime_info2": serializer2.data,
                "anime_info3": serializer3.data
            }
            except:
                response_data = {
                "anime_info": serializer.data,
                "anime_info2": serializer2.data,
                "anime_info3": False
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
            if score_table.status == "просмотренно":
                return Response("просмотренно")
            elif score_table.status == "запланированно":
                return Response("запланированно")
            elif score_table.status == "брошенно":
                return Response("брошенно")
            
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
