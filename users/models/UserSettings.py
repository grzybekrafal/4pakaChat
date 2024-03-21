# -*- coding: utf-8 -8-
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.cache import cache

class UserSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user")
    image = models.FileField(upload_to='user_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super(UserSettings, self).save(*args, **kwargs)  # Call the "real" save() method
        cache.clear()

    def __str__(self):
        return f"{self.user.id}"

    class Meta:
        verbose_name_plural = "Images"

User.settings = property(lambda u: UserSettings.objects.get_or_create(user=u)[0])