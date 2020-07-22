# from rest_framework_jwt.views import ObtainJSONWebToken
from dataserver.models import UserLabelData
from rest_framework import serializers


class UserLabelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLabelData
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

