from rest_framework import serializers
from .models import CryptUser
from .algorythm import RSA


class RegisterUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CryptUser
        fields = ['username', 'user_key_module', 'user_key_exponent']

    def save(self):
        e, n, d = RSA().generate_keys()
        user = CryptUser(username=self.validated_data['username'],
                         server_key_module=n, server_key_exponent=e, server_key_D=d,
                         user_key_module=self.validated_data['user_key_module'],
                         user_key_exponent=self.validated_data['user_key_exponent']
                         )

        user.save()

        return user


class ChatSerializer(serializers.HyperlinkedModelSerializer):

    text = serializers.CharField()

    class Meta:
        model = CryptUser
        fields = ['username', 'text']

