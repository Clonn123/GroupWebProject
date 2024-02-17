from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Animes
from .serializer import MyModelSerializer

class MyAPIView(APIView): 
    def get(self, request):
        data_list = Animes.objects.all()
        serializer = MyModelSerializer(data_list, many=True)
        return Response(serializer.data)
