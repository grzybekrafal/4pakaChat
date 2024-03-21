# -*- coding: utf-8 -8-
import random
import string

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.cache import cache

class UserRegeneratePassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_regenerate")
    token_regenerate = models.CharField(null=False, blank=False, max_length=35, unique=True)
    active = models.BooleanField(default=True, blank=False)
    create = models.DateField(null=False, blank=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        super(UserRegeneratePassword, self).save(*args, **kwargs)
        cache.clear()
    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name_plural = "Token"

User.settings = property(lambda u: UserRegeneratePassword.objects.get_or_create(user=u)[0])