# from rest_framework_jwt.views import ObtainJSONWebToken

from tileserver.models import Map, MapData
from rest_framework import serializers


class CstdMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'
        # fields = ['id', 'username', 'email', 'phone']


class MapDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapData
        fields = '__all__'


class MapDataUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapData
        fields = ['id', 'name', 'author', 'author_id', 'is_deleted', 'description', 'create_time', 'end_time']

        # fields = ['name', 'author', 'author_id']
        # # fields = ['id', 'name']
        # fields = ['id', 'name', 'author', 'author_id', 'description', 'is_deleted', 'create_time', 'end_time']
        # read_only_fields = ['account_name']
        # fields = '__all__'

    # def create(self, validated_data):
    #     mapdata = MapData.objects.create(**validated_data)
    #     print('hehhe:', mapdata)
    #     return mapdata
    # def save(self, validated_data):
    #     mapData = MapData(validated_data)
    #     mapData.save()
    #     return mapData

