from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer, ChatSerializer
from .models import CryptUser
from .algorythm import RSA


@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user'
            data['username'] = account.username
            data['server_exponent'] = account.server_key_exponent
            data['server_module'] = account.server_key_module
        else:
            data = serializer.errors
        return Response(data)


@api_view(['GET',])
def chat_view(request):
    if request.method == 'GET':
        data = {}
        if request.data['username'] is not None and request.data['text'] is not None:
            user = CryptUser.objects.get(username=request.data['username'])

            text = ''
            for letter in request.data['text']:
                lett = RSA().decrypt(letter, user.server_key_D, user.server_key_module)
                text += lett

            result = ''
            for letter in text.capitalize():
                result += RSA().encrypt(letter, user.user_key_exponent, user.user_key_module)

            data['text'] = result
            
        else:
            data['error'] = 'blank username or text'
        return Response(data)


#
# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = CryptUser.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = []
#
#
# class ChatView(APIView):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = CryptUser.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = []
#
#     def get(self, request, format=None):
#         print(request)
