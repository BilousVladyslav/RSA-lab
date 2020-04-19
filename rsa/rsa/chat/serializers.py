from .models import CryptUser
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CryptUser
        fields = ['username', 'user_key_module', 'user_key_exponent']