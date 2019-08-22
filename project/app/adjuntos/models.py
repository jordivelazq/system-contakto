# -*- coding: utf-8 -*-
from django.db import models
from app.investigacion.models import Investigacion
from image_functions import ImgOpt
from django.db.models.signals import post_save
from django.conf import settings
from django.core.exceptions import ValidationError
import os

class Adjuntos(models.Model):
	investigacion = models.ForeignKey(Investigacion)
	adj1 = models.FileField(verbose_name='Solicitud o currículum (.doc,.pdf,.jpg)', upload_to='adj', blank=True, null=True)
	adj2 = models.FileField(verbose_name='Foto Candidato', upload_to='adj', blank=True, null=True)
	adj3 = models.FileField(verbose_name='Foto Interior 1', upload_to='adj', blank=True, null=True)
	adj4 = models.FileField(verbose_name='Foto Interior 2', upload_to='adj', blank=True, null=True)
	adj5 = models.FileField(verbose_name='Foto Exterior', upload_to='adj', blank=True, null=True)
	adj6 = models.FileField(verbose_name='Foto tipo face', upload_to='adj', blank=True, null=True)
	adj7 = models.FileField(verbose_name='Validación de Demandas Laborales', upload_to='adj', blank=True, null=True)
	adj8 = models.FileField(verbose_name='Semanas Cotizadas', upload_to='adj', blank=True, null=True)
	adj9 = models.FileField(verbose_name='Anexo 3. Exterior derecho', upload_to='adj', blank=True, null=True)
	adj10 = models.FileField(verbose_name='Anexo 4. Gestor Entrevistador', upload_to='adj', blank=True, null=True)
	adj11 = models.FileField(verbose_name='Anexo 5. Aviso Privacidad', upload_to='adj', blank=True, null=True)
	adj12 = models.FileField(verbose_name='Anexo 6. Constancia', upload_to='adj', blank=True, null=True)
	adj13 = models.FileField(verbose_name='Croquis', upload_to='adj', blank=True, null=True)
	adj14 = models.FileField(verbose_name='Ultimo grado de estudios', upload_to='adj', blank=True, null=True)
	adj15 = models.FileField(verbose_name='Anexo', upload_to='adj', blank=True, null=True)
	adj16 = models.FileField(verbose_name='Comprobante de domicilio', upload_to='adj', blank=True, null=True)
	adj17 = models.FileField(verbose_name='Acta de nacimiento', upload_to='adj', blank=True, null=True)
	adj18 = models.FileField(verbose_name='Extra', upload_to='adj', blank=True, null=True)

	def filename(self):
		return os.path.basename(self.file.name)

	def __unicode__(self):
		return u'%s' % self.investigacion

def resize_adjuntos(sender, **kwargs):
	#adj2
	if len(str(kwargs['instance'].adj2)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj2), size_x=800)
	#adj3
	if len(str(kwargs['instance'].adj3)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj3), size_x=800)
	#adj4
	if len(str(kwargs['instance'].adj4)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj4), size_x=800)
	#adj5
	if len(str(kwargs['instance'].adj5)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj5), size_x=800)
	#adj6
	if len(str(kwargs['instance'].adj6)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj6), size_x=800)
	#adj7
	if len(str(kwargs['instance'].adj7)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj7), size_x=800)
	#adj8
	if len(str(kwargs['instance'].adj8)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj8), size_x=800)
	#adj9
	if len(str(kwargs['instance'].adj9)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj9), size_x=800)
	#adj10
	if len(str(kwargs['instance'].adj10)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj10), size_x=800)
	#adj11
	if len(str(kwargs['instance'].adj11)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj11), size_x=800)
	#adj12
	if len(str(kwargs['instance'].adj12)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj12), size_x=800)
	#adj13
	if len(str(kwargs['instance'].adj13)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj13), size_x=800)
	#adj14
	if len(str(kwargs['instance'].adj14)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj14), size_x=800)
	if len(str(kwargs['instance'].adj15)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj15), size_x=800)
	if len(str(kwargs['instance'].adj16)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj16), size_x=800)
	if len(str(kwargs['instance'].adj17)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj17), size_x=800)
	if len(str(kwargs['instance'].adj18)):
		ImgOpt.resize(file_path=settings.MEDIA_ROOT+'/'+str(kwargs['instance'].adj18), size_x=800)

post_save.connect(resize_adjuntos, sender=Adjuntos)
