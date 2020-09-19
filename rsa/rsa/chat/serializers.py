from rest_framework import serializers
from .models import CryptUser
from .algorythm import RSA


class RegisterUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CryptUser
        fields = ['username', 'user_key_module', 'user_key_exponent']

    def save(self):
        e, n, d = RSA().generate_keys()

        while d is None:
            e, n, d = RSA().generate_keys()

        user = CryptUser(username=self.validated_data['username'],
                         server_key_module=n, server_key_exponent=e, server_key_D=d,
                         user_key_module=self.validated_data['user_key_module'],
                         user_key_exponent=self.validated_data['user_key_exponent']
                         )

        user.save()

        return user


class ChatSerializer(serializers.Serializer):

    text = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        fields = ['username', 'text']

    def get_data(self):
        username = self.validated_data['username']
        users_queryset = CryptUser.objects.filter(username=username)

        if len(users_queryset) == 0:
            raise serializers.ValidationError({'error': 'User does not exist.'})

        return users_queryset[0], self.validated_data['text']

