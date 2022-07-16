# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from app.core.models import Estado, Municipio

ACTIVO_OPCIONES = (
        (0, 'Sí/No'),
        (1, 'Sí'),
        (2, 'No'),
    )

class Compania(models.Model):
    nombre = models.CharField(max_length=140, verbose_name='Nombre comercial')  #CHECK
    telefono = models.CharField(max_length=20, verbose_name='Teléfono', blank=True, null=True)
    telefono_alt = models.CharField(max_length=20, verbose_name='Teléfono Alterno', blank=True, null=True)
    email = models.EmailField(max_length=140, verbose_name='Correo', blank=True, null=True) #CHECK
    role = models.CharField(max_length=140, verbose_name='Giro', blank=True, null=True) #CHECK
    rfc_direccion = models.CharField(max_length=250, verbose_name='Dirección Fiscal', blank=True, null=True) #CHECK
    rfc = models.CharField(max_length=20, verbose_name='RFC', blank=True, null=True) #CHECK
    notas = models.TextField(verbose_name='Notas', blank=True, null=True) #CHECK
    es_cliente = models.BooleanField(default=True, verbose_name='Es cliente') #CHECK
    razon_social = models.CharField(max_length=500, verbose_name='Razón social', blank=True, null=True)  #CHECK
    referencia_correo = models.IntegerField(default=0, verbose_name='Referencia por correo', choices=ACTIVO_OPCIONES, blank=True, null=True)

    coordinador_ejecutivos = models.ForeignKey(User, 
        blank=True, null=True, verbose_name='Coordinador de ejecutivos', on_delete=models.CASCADE, related_name='coordinador_ejecutivos')

    fecha_creacion = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return u'%s' % (self.nombre)

    class Meta:
        verbose_name = 'Compañia'

class Sucursales(models.Model):
    compania = models.ForeignKey(Compania, on_delete=models.CASCADE, related_name='sucursales')
    nombre = models.CharField(max_length=140, verbose_name='Sucursal')
    ciudad = models.CharField(max_length=140, verbose_name='Ciudad', blank=True, null=True)
    telefono = models.CharField(max_length=20, verbose_name='Teléfono', blank=True, null=True)
    email = models.EmailField(max_length=140, verbose_name='Correo', blank=True, null=True)

    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, blank=True, null=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.nombre)


class RegimenFiscal(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=140, verbose_name='Regimen Fiscal')
   
    def __str__(self):
        return u'%s' % (self.nombre)


class DireccionFiscal(models.Model):
    compania = models.ForeignKey(Compania, on_delete=models.CASCADE, related_name='direcciones_fiscales')
    regimen_fiscal = models.ForeignKey(RegimenFiscal, on_delete=models.CASCADE, related_name='regimen_fiscal')
    rfc = models.CharField(max_length=14, verbose_name='RFC')
    nombre = models.CharField(max_length=140, verbose_name='Nombre')
    direccion = models.CharField(max_length=140, verbose_name='Dirección', blank=True, null=True)
    codigo_postal = models.CharField(max_length=5, verbose_name='Código postal', blank=True, null=True)
   
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name='Estado')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name='Municipio')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return u'%s' % (self.nombre)


class Contacto(models.Model):
    compania = models.ForeignKey(Compania, related_name='compania_contacto', on_delete=models.CASCADE)

    nombre = models.CharField(max_length=140)
    puesto = models.CharField(max_length=140, blank=True, null=True)
    email = models.EmailField(max_length=250, verbose_name='Correo')
    email_alt = models.EmailField(max_length=250, verbose_name='Correo alterno', blank=True, null=True)
    telefono = models.CharField(max_length=20, verbose_name='Teléfono', blank=True, null=True)
    telefono_celular = models.CharField(max_length=20, verbose_name='Teléfono celular', blank=True, null=True)
    telefono_otro = models.CharField(max_length=20, verbose_name='Otro', blank=True, null=True)
    
    costo_inv_laboral = models.FloatField(verbose_name='Costo de investigación laboral', blank=True, null=True)
    costo_inv_completa = models.FloatField(verbose_name='Costo de investigación completa', blank=True, null=True)
    
    status = models.BooleanField(default=True)

    def __str__(self):
        return u'%s' % (self.nombre)

    class Meta:
        verbose_name = 'Contacto'
