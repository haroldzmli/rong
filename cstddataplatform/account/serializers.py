from account.models import CstdUser
from rest_framework import serializers


class CstdUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CstdUser
        # fields = ['id', 'username', 'email', 'phone']
        fields = '__all__'
