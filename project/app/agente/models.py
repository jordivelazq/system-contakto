from django.db import models
from django.contrib.auth.models import User


class AgenteInfo(models.Model):
	agente = models.ForeignKey(User, on_delete=models.CASCADE)
	telefono = models.CharField(max_length=150, blank=True, null=True)

	def __str__(self):
		return u'%s' % (self.agente.username)

class Labels(models.Model):
	LABEL_OPTIONS = (
		('LightPink', 'LightPink'),
		('Purple', 'Purple'),
		('Coral', 'Coral'),
		('Crimson', 'Crimson'),
		('LightGreen', 'LightGreen'),
		('ForestGreen', 'ForestGreen'),
		('LightSkyBlue', 'LightSkyBlue'),
		('DarkBlue', 'DarkBlue'),
		('Gold', 'Gold'),
		('Sienna', 'Sienna')
	)

	agente = models.ForeignKey(User, on_delete=models.CASCADE)
	color = models.CharField(max_length=100, choices=LABEL_OPTIONS)
	name = models.CharField(max_length=150, verbose_name='')

	def __str__(self):
		return u'%s' % (self.name)
