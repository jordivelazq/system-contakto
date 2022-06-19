from django.db import models
from django.contrib.auth.models import User


class Estado(models.Model):
    efe_key = models.CharField(max_length=3, primary_key=True, unique=True)
    estado = models.CharField(max_length=30)

    def __str__(self):
        return self.estado


class Municipio(models.Model):
    efe_key = models.ForeignKey(Estado, on_delete=models.CASCADE)
    municipio = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.municipio



class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messajes')
    title = models.CharField('Title', max_length=200)
    message = models.TextField('Message')
    link = models.CharField('Link', max_length=200, default='', blank=True, null=True)
    unread = models.BooleanField(default=True)
    trash = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)