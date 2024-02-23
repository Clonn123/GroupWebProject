from rest_framework import serializers
from .models import Animes
from .models import Users

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animes
        fields = '__all__'


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            'name': instance.name,
            'surname': instance.surname,
            'username': instance.username,
            'password': instance.password,
            'email': instance.email,
            'gender': instance.gender,
            'age': instance.age,
        }
        return representation
