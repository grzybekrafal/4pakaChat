# -*- coding: utf-8 -8-
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.cache import cache

class UsersPermision(models.Model):
    token_for_activate = models.CharField(max_length=550)
    token_is_used = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    regulations = models.BooleanField(default=True)
    marketing_conditions = models.BooleanField(default=True)
    privacy_policy = models.BooleanField(default=True)
    center_of_messagess = models.BooleanField(default=False)
    sms_agreement = models.BooleanField(default=False)
    email_agreement = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.token_is_used}"

    class Meta:
        verbose_name_plural = "Lista Kontaktów"
    def save(self, *args, **kwargs):
        super(UsersPermision, self).save(*args, **kwargs)  # Call the "real" save() method
        cache.clear()