from .router import router
from django.urls import re_path as url
from django.urls import path, include
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    path('users/', include(router.urls)),
]
