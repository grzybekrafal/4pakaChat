from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from ..models import Chat


class ChatRequestForHelp(models.Model):
    sender = models.ForeignKey(User, related_name='help_requests', on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, related_name='help_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)
    response = models.TextField(blank=True, null=True)
    models.DateTimeField(auto_now_add=True)
    handler_id = models.ForeignKey(User, related_name='help_handlers', on_delete=models.SET_NULL, blank=True, null=True)