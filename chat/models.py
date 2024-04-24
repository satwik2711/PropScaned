from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} in {self.chatroom.name}: {self.message}"

class BlockedUser(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    blocked_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.blocked_user.username} blocked in {self.chatroom.name}"