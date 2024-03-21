from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from ..models import Messages
from ..serializer.MessageForEditSerializer import MessageForEditSerializer
from ..serializer.MessageSerializer import MessageSerializer


class AddMessageViewSet(viewsets.ViewSet):
    '''
    POST

    CReate new message
    FIELDS
     'sender' -> user_id  not null
     'receiver' -> user_id not null
     'chat' -> chat_id not null
     'content' -> text
     'file' -> file ->  can be null
     'image' -> file ->  can be null

    '''

    def create(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@action(detail=True, methods=['get'])
class GetMessages(viewsets.ViewSet):
    '''
    GET

    Get message from chat
    chat_id -> chat_id
    offset -> int ->   can be null -> id null then 0
    limit -> int ->   can be null -> if null then 50
    '''
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
    '''
    POST

    Create request for help from user
    chat_id -> chat_id
    content -> text
    user must be login -> userid from user logging
    '''
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


class DeleteMessageViewSet(viewsets.ViewSet):
    '''
    POST

    Delete message
    FIELDS
    'id' - message id
    'chat' -> chat_id not null
    user must be login -> userid from user logging - for delete user_id == sender_id
    '''
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, pk=None):

        chat = request.POST.get('chat', 0)
        id = request.POST.get('id', 0)
        print(id)
        print(request.user)
        print(chat)

        message = get_object_or_404(Messages, pk=id, sender=request.user, chat_id=chat)
        message.delete()

        return Response(status=status.HTTP_200_OK)


class EditMessageViewSet(viewsets.ViewSet):
    '''
    POST

    Edit  message
    FIELDS
     'id' - message id
     'chat' -> chat_id not null
     'content' -> text
     user must be login -> userid from user logging - for delete user_id == sender_id
    '''
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, pk=None):
        chat = request.POST.get('chat', 0)
        id = request.POST.get('id', 0)

        message = get_object_or_404(Messages, pk=id, sender=request.user, chat_id=chat)
        serializer = MessageForEditSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
