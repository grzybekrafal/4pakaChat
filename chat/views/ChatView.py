from rest_framework import status, viewsets, authentication, permissions
from rest_framework.decorators import api_view, action, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from ..models import Chat
from ..serializer.ChatSerializer import ChatSerializer

class CreateChatViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@action(detail=True, methods=['get'])
class ChatList(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    def list(self, request):
        if request.method == 'GET':
            unread_counts = Chat.get_unread_message_counts(request.user.id)
            response_data = {
                'chats': unread_counts,
                'user_id': request.user.id,
            }
            return Response(response_data)
        return Response(status=status.HTTP_400_BAD_REQUEST)