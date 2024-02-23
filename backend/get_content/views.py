from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Animes
from .models import Users
from .serializer import MyModelSerializer
from .serializer import UserModelSerializer
from django.contrib.auth import get_user_model
from rest_framework.request import Request

# Users = get_user_model()

class DataAPIView(APIView): 
    def get(self, request):
        data_list = Animes.objects.all()
        serializer = MyModelSerializer(data_list, many=True)
        return Response(serializer.data)

class LoginAPIView(APIView): 
    def get(self, request):
        data_list = Users.objects.all()
        serializer = UserModelSerializer(data_list, many=True)
        return Response(serializer.data)

    # def user(request: Request):
    #     return Response({
    #         'data': UserModelSerializer(request.user).data
    #     })
    
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
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
