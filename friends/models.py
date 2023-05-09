from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=10, null=True, default=None)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"User {self.username} with id: {self.id}"


class FriendRequest(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipient')

    class Meta:
        verbose_name = 'Friend request'
        verbose_name_plural = 'Friend requests'
        unique_together = ('sender', 'recipient',)

    def __str__(self):
        return f"Request from {self.sender.username} to {self.recipient.username}"
