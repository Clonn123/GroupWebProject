from rest_framework import serializers
from .models import Animes, Anime_info, Score
from .models import Mangas, Manga_info, Score_manga
from .models import Users

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animes
        fields = '__all__'
class MangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mangas
        fields = '__all__'
class InfoAnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime_info
        fields = '__all__'
class InfoMangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga_info
        fields = '__all__'
        
class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'
    def to_representation(self, instance):
        representation = {
            'anime_id': instance.anime_id,
            'user_id': instance.user_id,
            'status': instance.status,
            'score': instance.score,
        }
        return representation
    
class ScoreMangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score_manga
        fields = '__all__'
    def to_representation(self, instance):
        representation = {
            'manga_id': instance.manga_id,
            'user_id': instance.user_id,
            'status': instance.status,
            'score': instance.score,
        }
        return representation

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
