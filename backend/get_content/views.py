from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Animes
from .models import Users
from .models import UserProfile
from .serializer import MyModelSerializer
from .serializer import UserModelSerializer
from rest_framework.request import Request
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken

class DataAPIView(APIView): 
    def get(self, request):
        data_list = Animes.objects.all()
        serializer = MyModelSerializer(data_list, many=True)
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
            # Генерируем JWT-токен
            refresh = RefreshToken.for_user(user)
            # refresh['identifier'] = user.identifier
            # refresh['name'] = user.name
            # refresh['surname'] = user.surname
            # refresh['username'] = user.username
            # refresh['password'] = user.password
            # refresh['email'] = user.email
            # refresh['gender'] = user.gender
            # refresh['age'] = user.age
            # refresh['birthdate'] = user.birthdate
            # refresh['photo'] = user.photo
            serializer = UserModelSerializer(user)
            # return Response(serializer.data)
            return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
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

class UserDetailView(APIView):
    def get(self, request, user_id):
        try:
            user = Users.objects.get(id=user_id)
            serializer = UserModelSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

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
