from django.db import models
from django.contrib.auth.models import User

class AgenteInfo(models.Model):
	agente = models.ForeignKey(User)
	telefono = models.CharField(max_length=150, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.agente.username)