from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from ..models import UserSettings

class UserSettingsSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.all())
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = UserSettings
        fields = ['id', 'image', 'user_id', 'username', 'email', 'first_name', 'last_name']
