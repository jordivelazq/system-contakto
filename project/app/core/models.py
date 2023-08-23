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


class TipoInvestigacionCosto(models.Model):

    TIPO_INVESTIGACION_OPCIONES = (
        (1, 'Laboral'),
        (2, 'Socioeconómico'),
        (4, 'Psicometrías'),
        (5, 'Visita Domiciliaria'),
        (7, 'Visita Domiciliaria con demandas'),
        (6, 'Validación de Demandas'),
    )

    tipo_investigacion = models.IntegerField(
        choices=TIPO_INVESTIGACION_OPCIONES, null=True, blank=True)
    costo = models.FloatField(default=0)

    # def __str__(self):
    #     return self.tipo_investigacion + " - " + str(self.costo)


class UserMessage(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_messajes')
    title = models.CharField('Title', max_length=200)
    message = models.TextField('Message')
    link = models.CharField('Link', max_length=200,
                            default='', blank=True, null=True)
    unread = models.BooleanField(default=True)
    trash = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
