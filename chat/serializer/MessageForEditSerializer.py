from rest_framework import serializers
from ..models import Messages

class MessageForEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['id','content',]