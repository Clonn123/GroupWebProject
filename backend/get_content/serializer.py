from rest_framework import serializers
from .models import Animes, Anime_info, Score
from .models import Users

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animes
        fields = '__all__'
class InfoAnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime_info
        fields = '__all__'
class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            'identifier': instance.identifier,
            'name': instance.name,
            'surname': instance.surname,
            'username': instance.username,
            'password': instance.password,
            'email': instance.email,
            'gender': instance.gender,
            'age': instance.age,
            'birthdate': instance.birthdate,
            'photo': instance.photo.url if instance.photo else None, 
        }
        return representation
