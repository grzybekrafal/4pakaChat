from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage
from django.db import models
from django.contrib.auth.models import User
from ..models import Chat, ChatRequestForHelp
from django.db.models import Count, Q

class Messages(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver_messages', on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, related_name='chat', on_delete=models.CASCADE)
    content = models.TextField()
    file = models.FileField(upload_to='message_files/', blank=True, null=True)
    image = models.FileField(upload_to='message_images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    chat_request_for_help = models.OneToOneField(ChatRequestForHelp, related_name='message_request_for_help', on_delete=models.SET_NULL,
                                                 blank=True, null=True)



    def __str__(self):
        return f"{self.sender.username} - {self.chat.topic}"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        self.chat.last_message_at = self.timestamp
        self.chat.save(update_fields=['last_message_at'])

    @staticmethod
    def get_messages(chat, user_id, offset, limit):
        messages = Messages.objects.filter(chat=chat).order_by('-timestamp')

        try:
            limit = int(limit)
        except (TypeError, ValueError):
            limit = 0

        if limit == 0:
            limit = 50

        try:
            offset = int(offset)
        except (TypeError, ValueError):
            offset = 0


        paginator = Paginator(messages, limit)

        try:
            messages = paginator.page(offset // limit + 1)
        except EmptyPage:
            messages = []

        message_list = messages.object_list
        messages = message_list.values('id',
                                   'sender__id', 'sender__username',
                                   'receiver__id', 'receiver__username',
                                   'chat__id', 'chat__topic',
                                   'content', 'file', 'image', 'timestamp', 'is_read'
                                   )

        for m in messages:
            if str(m['receiver__id']) == user_id and m['is_read'] == 0:
                print('aktualizacja')
                Messages.objects.filter(pk=m['id']).update(is_read=True, read_at=timezone.now())

        return messages


    @staticmethod
    def add_message(chat_id, sender_id, content, file=None, image=None):
        chat = Chat.objects.get(pk=chat_id)
        if not chat.created_by_id == sender_id and not chat.recipient_id == sender_id:
            raise ValueError("Sender is not a member of this chat")

        new_message = Messages.objects.create(
            sender_id=sender_id,
            receiver_id=chat.recipient_id,
            chat_id=chat_id,
            content=content,
            file=file,
            image=image,
            timestamp=timezone.now(),
            is_read=False,
            read_at=None
        )

        chat.last_message_at = new_message.timestamp
        chat.save(update_fields=['last_message_at'])

        return new_message

    @staticmethod
    def get_unread_messages(user_id):
        unread_messages_info = list(Messages.objects.filter(
            receiver__id=user_id,
            is_read=False
        ).values('chat__id').annotate(unread_count=Count('id')))
        unread_messages = [{'id': info['chat__id'], 'unread': info['unread_count']} for info in unread_messages_info]
        return unread_messages

    @staticmethod
    def request_for_help(sender_id, chat_id, content):
        chat = Chat.objects.get(pk=chat_id)
        if not chat.created_by_id == sender_id and not chat.recipient_id == sender_id:
            raise ValueError("User is not a member of this chat")

        chat_request_for_help = ChatRequestForHelp.objects.create(
            sender_id=sender_id,
            chat_id=chat_id,
            response='',
            timestamp=timezone.now(),
        )

        new_message = Messages.objects.create(
            sender_id=sender_id,
            receiver_id=chat.recipient_id,
            chat_id=chat_id,
            content=content,
            file=None,
            image=None,
            timestamp=timezone.now(),
            is_read=False,
            read_at=None,
            chat_request_for_help_id=chat_request_for_help.id
        )

        chat.last_message_at = new_message.timestamp
        chat.save(update_fields=['last_message_at'])

        return new_message


