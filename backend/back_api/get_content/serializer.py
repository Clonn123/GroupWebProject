from rest_framework import serializers
from .models import Animes

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animes
        fields = '__all__'
