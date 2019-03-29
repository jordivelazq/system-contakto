from django.db import models
from django.contrib.auth.models import User

class Bitacora(models.Model):
	action = models.CharField(max_length=120, default='')
	user = models.ForeignKey(User)
	datetime = models.DateTimeField(auto_now_add=True)
