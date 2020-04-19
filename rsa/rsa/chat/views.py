from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import CryptUser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CryptUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = []