# -*- coding: utf-8 -*-
from django.db import models
from app.investigacion.models import Investigacion
from app.adjuntos.image_functions import ImgOpt
from django.db.models.signals import post_save
from django.conf import settings
from django.core.exceptions import ValidationError
import os

class Adjuntos(models.Model):
	investigacion = models.ForeignKey(Investigacion)
	adj2 = models.FileField(verbose_name='1. Foto de perfil del candidato', upload_to='adj', blank=True, null=True)

	adj3 = models.FileField(verbose_name='2.a Interior derecho', upload_to='adj', blank=True, null=True)
	adj4 = models.FileField(verbose_name='2.b Interior izquierdo', upload_to='adj', blank=True, null=True)
	adj5 = models.FileField(verbose_name='2.c Exterior derecho', upload_to='adj', blank=True, null=True)
	adj6 = models.FileField(verbose_name='2.d Exterior izquierdo', upload_to='adj', blank=True, null=True)
	adj9 = models.FileField(verbose_name='2.e Frente', upload_to='adj', blank=True, null=True)

	adj10 = models.FileField(verbose_name='3. Gestor Entrevistador', upload_to='adj', blank=True, null=True)
	adj13 = models.FileField(verbose_name='4. Croquis', upload_to='adj', blank=True, null=True)
	adj11 = models.FileField(verbose_name='5. Aviso Privacidad', upload_to='adj', blank=True, null=True)
	adj12 = models.FileField(verbose_name='6. Constancia', upload_to='adj', blank=True, null=True)
	
	adj14 = models.FileField(verbose_name='7.a Identificación con fotografia', upload_to='adj', blank=True, null=True)
	adj22 = models.FileField(verbose_name='7.b Identificación con fotografia', upload_to='adj', blank=True, null=True)
	adj23 = models.FileField(verbose_name='7.c Identificación con fotografia', upload_to='adj', blank=True, null=True)
	adj24 = models.FileField(verbose_name='7.d Identificación con fotografia', upload_to='adj', blank=True, null=True)

	adj17 = models.FileField(verbose_name='8. Acta de nacimiento', upload_to='adj', blank=True, null=True)
	adj16 = models.FileField(verbose_name='9. Comprobante de domicilio', upload_to='adj', blank=True, null=True)
	
	adj8 = models.FileField(verbose_name='10.a Semanas Cotizadas', upload_to='adj', blank=True, null=True)
	adj25 = models.FileField(verbose_name='10.b Semanas Cotizadas', upload_to='adj', blank=True, null=True)
	adj26 = models.FileField(verbose_name='10.c Semanas Cotizadas', upload_to='adj', blank=True, null=True)
	adj27 = models.FileField(verbose_name='10.d Semanas Cotizadas', upload_to='adj', blank=True, null=True)
	adj28 = models.FileField(verbose_name='10.e Semanas Cotizadas', upload_to='adj', blank=True, null=True)

	adj7 = models.FileField(verbose_name='11.a Validación de Demandas Laborales', upload_to='adj', blank=True, null=True)
	adj36 = models.FileField(verbose_name='11.b Validacion web', upload_to='adj', blank=True, null=True)
	
	adj18 = models.FileField(verbose_name='Carta Laboral', upload_to='adj', blank=True, null=True)
	adj19 = models.FileField(verbose_name='Adicionales A', upload_to='adj', blank=True, null=True)
	adj20 = models.FileField(verbose_name='Adicionales B', upload_to='adj', blank=True, null=True)
	adj21 = models.FileField(verbose_name='Adicionales C', upload_to='adj', blank=True, null=True)

	adj29 = models.FileField(verbose_name='Adicionales D', upload_to='adj', blank=True, null=True)
	adj30 = models.FileField(verbose_name='Adicionales E', upload_to='adj', blank=True, null=True)
	adj31 = models.FileField(verbose_name='Adicionales F', upload_to='adj', blank=True, null=True)
	adj32 = models.FileField(verbose_name='Adicionales G', upload_to='adj', blank=True, null=True)
	adj33 = models.FileField(verbose_name='Adicionales H', upload_to='adj', blank=True, null=True)
	adj34 = models.FileField(verbose_name='Adicionales I', upload_to='adj', blank=True, null=True)

	adj35 = models.FileField(verbose_name='Extra A', upload_to='adj', blank=True, null=True)

	def filename(self):
		return os.path.basename(self.file.name)

	def __str__(self):
		return u'%s' % self.investigacion

def resize_adjuntos(sender, **kwargs):
	#adj2
	if len(str(kwargs['instance'].adj2)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj2), size_x=1600)
	#adj3
	if len(str(kwargs['instance'].adj3)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj3), size_x=1600)
	#adj4
	if len(str(kwargs['instance'].adj4)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj4), size_x=1600)
	#adj5
	if len(str(kwargs['instance'].adj5)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj5), size_x=1600)
	#adj6
	if len(str(kwargs['instance'].adj6)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj6), size_x=1600)
	#adj7
	if len(str(kwargs['instance'].adj7)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj7), size_x=1600)
	#adj36
	if len(str(kwargs['instance'].adj36)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj36), size_x=1600)
	#adj8
	if len(str(kwargs['instance'].adj8)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj8), size_x=1600)
	#adj9
	if len(str(kwargs['instance'].adj9)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj9), size_x=1600)
	#adj10
	if len(str(kwargs['instance'].adj10)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj10), size_x=1600)
	#adj11
	if len(str(kwargs['instance'].adj11)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj11), size_x=1600)
	#adj12
	if len(str(kwargs['instance'].adj12)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj12), size_x=1600)
	#adj13
	if len(str(kwargs['instance'].adj13)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj13), size_x=1600)
	#adj14
	if len(str(kwargs['instance'].adj14)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj14), size_x=1600)
	
	if len(str(kwargs['instance'].adj16)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj16), size_x=1600)
	if len(str(kwargs['instance'].adj17)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj17), size_x=1600)
	
	if len(str(kwargs['instance'].adj18)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj18), size_x=1600)
	if len(str(kwargs['instance'].adj19)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj19), size_x=1600)
	if len(str(kwargs['instance'].adj20)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj20), size_x=1600)
	if len(str(kwargs['instance'].adj21)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj21), size_x=1600)
	
	if len(str(kwargs['instance'].adj29)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj29), size_x=1600)
	if len(str(kwargs['instance'].adj30)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj30), size_x=1600)
	if len(str(kwargs['instance'].adj31)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj31), size_x=1600)
	if len(str(kwargs['instance'].adj32)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj32), size_x=1600)
	if len(str(kwargs['instance'].adj33)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj33), size_x=1600)
	if len(str(kwargs['instance'].adj34)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj34), size_x=1600)

post_save.connect(resize_adjuntos, sender=Adjuntos)
