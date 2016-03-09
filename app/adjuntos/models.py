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
	adj7 = models.FileField(verbose_name='Anexo 1', upload_to='adj', blank=True, null=True)
	adj8 = models.FileField(verbose_name='Anexo 2', upload_to='adj', blank=True, null=True)
	adj9 = models.FileField(verbose_name='Anexo 3', upload_to='adj', blank=True, null=True)
	adj10 = models.FileField(verbose_name='Anexo 4', upload_to='adj', blank=True, null=True)
	adj11 = models.FileField(verbose_name='Anexo 5', upload_to='adj', blank=True, null=True)
	adj12 = models.FileField(verbose_name='Anexo 6', upload_to='adj', blank=True, null=True)
	adj13 = models.FileField(verbose_name='Croquis', upload_to='adj', blank=True, null=True)

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

post_save.connect(resize_adjuntos, sender=Adjuntos)