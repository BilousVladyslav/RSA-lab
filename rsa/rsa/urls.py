from django.urls import include, path
from rest_framework import routers
from django.contrib import admin
from django.urls import path
from .chat.views import registration_view, chat_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', registration_view, name='register'),
    path('chat/', chat_view, name='chat'),
]
