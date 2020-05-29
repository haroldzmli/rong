from account.models import CstdUser, MapDataUser
from rest_framework import serializers


class CstdUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = CstdUser.objects.create_user(validated_data['phone'], validated_data['email'],
                                            validated_data['username'],validated_data['password'])
        return user

    class Meta:
        model = CstdUser
        # fields = ['id', 'username', 'email', 'phone']
        fields = '__all__'


class CstdUserRegistorSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = CstdUser.objects.create_user(validated_data['phone'], validated_data['email'],
                                            validated_data['username'], validated_data['password'])
        return user

    class Meta:
        model = CstdUser
        fields = ['id', 'username', 'email', 'phone',  'password', 'alias']


class MapDataUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MapDataUser
        # fields = ['user_id', 'map_data_id', 'start_time', 'end_time']
        fields = '__all__'
