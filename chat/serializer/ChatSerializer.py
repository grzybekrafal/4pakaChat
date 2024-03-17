from rest_framework import serializers
from ..models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'created_by', 'recipient', 'topic', 'created_at']
