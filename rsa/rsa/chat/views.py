from rest_framework.response import Response
from rest_framework.decorators import api_view
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


@api_view(['POST',])
def chat_view(request):
    print(request.data)
    if request.method == 'POST':
        data = {}
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            user, text = serializer.get_data()

            decrypted_text = RSA().decrypt_str(text, user.server_key_D, user.server_key_module)

            response_text = decrypted_text.upper()

            response = RSA().encrypt_str(response_text, user.user_key_exponent, user.user_key_module)

            data['text'] = response

        else:
            data = serializer.errors
        return Response(data)
