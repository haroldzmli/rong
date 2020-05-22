from tileserver.models import Map, MapData
from rest_framework import serializers


class CstdMapSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Map
        # fields = ['id', 'username', 'email', 'phone']


class MapDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapData
        fields = ['name']
