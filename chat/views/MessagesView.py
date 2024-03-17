from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from ..models import Messages
from ..serializer.MessageSerializer import MessageSerializer


class AddMessageViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@action(detail=True, methods=['get'])
class GetMessages(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    def list(self, request):
        if request.method == 'GET':

            chat_id = request.GET.get('chat_id', 0)
            offset = request.GET.get('offset', 0)
            limit = request.GET.get('limit', 0)

            from ..models.Chat import Chat
            chat = Chat.objects.get(pk=chat_id)
            if chat.created_by_id != request.user.id and chat.recipient_id != request.user.id:
                return Response({'error': "User is not a member of this chat"}, status=status.HTTP_400_BAD_REQUEST)

            messages = Messages.get_messages(request.user.id, chat_id, offset, limit)
            response_data = {
                messages
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@action(detail=True, methods=['post'])
class RequestForHelp(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    def create(self, request):

        if request.method == 'POST':
            chat_id = request.POST.get('chat_id', 0)
            content = request.POST.get('content', '')

            if content == '':
                return Response({'error': 'Content is empty'}, status=status.HTTP_400_BAD_REQUEST)
            if chat_id == 0:
                return Response({'error': 'Chat id is empty'}, status=status.HTTP_400_BAD_REQUEST)

            messages = Messages.request_for_help(request.user.id, chat_id, content)
            response_data = {
                'id': messages.id,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

