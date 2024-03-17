from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Q


class Chat(models.Model):
    created_by = models.ForeignKey(User, related_name='created_chats', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_chats', on_delete=models.CASCADE)
    topic = models.CharField(max_length=500)
    route_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

    def clean(self):
        super().clean()
        if self.created_by == self.recipient:
            raise ValidationError("Nie można tworzyć czatu z samym sobą")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @staticmethod
    def get_unread_message_counts(user_id):

        chats = list(Chat.objects.filter(Q(created_by_id=user_id) | Q(recipient_id=user_id))
                 .values('id', 'topic', 'route_id', 'created_by__id',
                         'created_by__username', 'recipient__id', 'recipient__username', 'last_message_at'))

        from ..models.Messages import Messages
        unread_messages = Messages.get_unread_messages(user_id)
        print(unread_messages)
        for item in chats:
            chat_id = item['id']
            item['unread'] = 0
            for unread in unread_messages:
                if unread['id'] == chat_id:
                    item['unread'] = unread['unread']

        return chats

    @staticmethod
    def create_chat( created_by_id, recipient_id, topic, route_id=None):
        created_by = User.objects.get(pk=created_by_id)
        recipient = User.objects.get(pk=recipient_id)

        new_chat = Chat.objects.create(
            created_by=created_by,
            recipient=recipient,
            topic=topic,
            route_id=route_id
        )

        return new_chat
