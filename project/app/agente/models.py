from pyexpat import model
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


class GestorInfo(models.Model):
	ESTATUS = (
		(1, 'ASPIRANTE'),
		(2, 'EN CAPACITACIÓN'),
		(3, 'PRUEBAS'),
		(4, 'ACTIVO'),
		(5, 'INACTIVO'),
	)

	TIPO_PAGO = (
		(1, "A"),
		(2, "B"),
		(3, "C"),
	)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	telefono = models.CharField(max_length=15, null=True, blank=True)
	ciudad = models.CharField(max_length=100, null=True, blank=True)
	estado = models.CharField(max_length=100, null=True, blank=True)
	zona = models.TextField(null=True, blank=True)
	fecha_ingreso = models.DateField()
	fecha_registro = models.DateTimeField(auto_now_add=True)
	estatus = models.PositiveSmallIntegerField(choices=ESTATUS, default=1)
	tipo_pago = models.PositiveSmallIntegerField(choices=TIPO_PAGO, default=1)

	def __str__(self):
		return '{} {} Tel:{} Ciudad:{} Estado:{} Zona: {} Tipo:{}'.format(self.usuario.first_name, self.usuario.last_name , self.telefono, self.ciudad, self.estado, self.zona, self.get_tipo_pago_display())
