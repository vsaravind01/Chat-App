from django.db import models
from datetime import datetime


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=25, primary_key=True)
    admin = models.CharField(max_length=25, null=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    msg = models.CharField(max_length=2000, null=False, editable=False)
    user = models.CharField(max_length=25)
    date = models.DateTimeField(auto_now_add=True)
