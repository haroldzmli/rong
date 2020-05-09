from tileserver.models import Map
from rest_framework import serializers


class CstdMapSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Map
        # fields = ['id', 'username', 'email', 'phone']
