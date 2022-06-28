from allauth.account.signals import user_logged_in
from app.compania.models import Compania
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User

from app.core.models import Estado, Municipio

def validate_nss(nss):
	if nss != '' and len(nss) != 11:
		raise ValidationError('NSS debe tener 11 caracteres')

def validate_curp(curp):
	if curp != '' and len(curp) != 18:
		raise ValidationError('CURP debe tener 18 caracteres')


class ClienteUser(User):

    telefono = models.CharField(max_length=20, blank=True)
    compania = models.ForeignKey(Compania, on_delete=models.CASCADE, null=True, blank=True)
    

    created = models.DateTimeField(auto_now=True, blank=True)
    modificated = models.DateTimeField(auto_now_add=True, blank=True)

    @property
    def get_compania(self):
        # c = Compania.objects.get(id=self.compania.id)
        # if c:
        #     return c.nombre
        # else:
        #     return None  
        return self.compania.nombre

    class Meta:
        verbose_name = 'CLiente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return u"%s" % self.first_name


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True)
    compania = models.ForeignKey(Compania, on_delete=models.CASCADE)

    def __str__(self):
        return u'%s / %s' % (self.user, self.compania)


class ClienteSolicitud(models.Model):
    cliente = models.ForeignKey(ClienteUser, on_delete=models.CASCADE, related_name='cliente_solicitud')
    enviado = models.BooleanField(default=False)

    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)


class ClienteSolicitudCandidato(models.Model):
    
    TIPO_INVESTIGACION_OPCIONES = (		
		(1, 'Laboral'),
		(2, 'Socioeconómico'),
		(4, 'Psicometrías'),
		(5, 'Visita Domiciliaria'),
		(7, 'Visita Domiciliaria con demandas'),
		(6, 'Validación de Demandas'),
	)
    
    STATUS_OPCIONES = (
		('0', 'En Investigación'),
		('1', 'Pdt. por Cliente'),
		('2', 'Inv. Terminada'),
	)

    cliente_solicitud = models.ForeignKey(ClienteSolicitud, on_delete=models.CASCADE, related_name="cliente_solicitud_candidato")


    nombre = models.CharField(max_length=140)
    apellido = models.CharField(max_length=140, default="")
    nss = models.CharField(max_length=30, default="None", validators=[validate_nss])
    email = models.CharField(max_length=140, blank=True, null=True)
    edad = models.IntegerField( blank=True, null=True) #choices=EDAD_CHOICES,
    curp = models.CharField(max_length=20, default="None", validators=[validate_curp])
    puesto = models.CharField(max_length=140, blank=True, null=True)

    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, blank=True, null=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, blank=True, null=True)

    status = models.CharField(max_length=140, choices=STATUS_OPCIONES, default='0')
    enviado = models.BooleanField(default=False)
    tipo_investigacion = models.IntegerField(choices=TIPO_INVESTIGACION_OPCIONES, default=2)

    archivo_solicitud = models.FileField(upload_to='cliente_solicitudes/', blank=True, null=True)
    
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

