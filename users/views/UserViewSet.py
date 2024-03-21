from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from ..serializer import *
from ..filters import *
from ..models import *


class UserViewSet(viewsets.ViewSet):
    '''
POST Create new user \n
GET list  of users\n\n
Fields:\n
    'id', 'username', 'email', 'first_name', 'last_name', 'is_staff'
    '''
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = None
        id = request.query_params.get('id', None)
        try:
            id = int(id)
        except (TypeError, ValueError):
            id = None

        if id is None:
            queryset = User.objects.all()
        else:
            queryset = User.objects.filter(pk=id)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class UserInfoViewSet(viewsets.ViewSet):
    '''
POST Add icon to user account \n
 Fields:\n
    user_id,  image
\n\n\n
GET list of user icon's to\n\n
Fields:\n
    ['id', 'image', 'user_id', 'username', 'email', 'first_name', 'last_name']
To serach one user
param user_id (int)
    '''
    def create(self, request):
        serializer = UserSettingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = None
        user_id = request.query_params.get('user_id', None)
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            user_id = None

        if user_id is None:
            queryset = UserSettings.objects.all()
        else:
            queryset = UserSettings.objects.filter(user_id=user_id)
        serializer = UserSettingsSerializer(queryset, many=True)
        return Response(serializer.data)




