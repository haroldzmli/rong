from account.models import CstdUser
from rest_framework import serializers


class CstdUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CstdUser
        fields = ['id', 'username', 'email', 'phone']
