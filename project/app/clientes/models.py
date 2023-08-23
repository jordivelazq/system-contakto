from app.compania.models import Compania, DireccionFiscal, Sucursales
from app.core.models import Estado, Municipio
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validate_nss(nss):
    if nss != '' and len(nss) != 11:
        raise ValidationError('NSS debe tener 11 caracteres')


def validate_curp(curp):
    if curp != '' and len(curp) != 18:
        raise ValidationError('CURP debe tener 18 caracteres')


class ClienteUser(User):

    telefono = models.CharField(max_length=20, blank=True)
    compania = models.ForeignKey(
        Compania, on_delete=models.CASCADE, null=True, blank=True)

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
        verbose_name = 'Cliente'
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
    cliente = models.ForeignKey(
        ClienteUser, on_delete=models.CASCADE,
        related_name='cliente_solicitud')
    enviado = models.BooleanField(default=False)

    # TODO: Colcoar estados segun la secuencia de la solicitud
    observaciones = models.TextField(blank=True)

    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    @property
    def get_candidatos_count(self):
        sc = ClienteSolicitudCandidato.objects.filter(
            cliente_solicitud_id=self.pk).count()
        return sc

    @property
    def get_candidatos_completados_count(self):

        from app.investigacion.models import Investigacion
        candidatos_completados = Investigacion.objects.filter(
            cliente_solicitud_id=self.pk,
            investigacion_completada=True).count()
        return candidatos_completados

    def __str__(self):
        return u'%s  (%s)' % (self.cliente, self.cliente.email)

    class Meta:
        ordering = ('-fecha_solicitud', )
        verbose_name = 'Solictud de Cliente'
        verbose_name_plural = 'Solictudes de Clientes'


class ClienteTipoInvestigacion(models.Model):

    tipo_investigacion = models.CharField(max_length=100)
    costo = models.FloatField(default=0)

    class Meta:
        ordering = ('tipo_investigacion', )

    def __str__(self):
        return u'%s' % (self.tipo_investigacion)


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

    cliente_solicitud = models.ForeignKey(
        ClienteSolicitud, on_delete=models.CASCADE,
        related_name="cliente_solicitud_candidato")

    nombre = models.CharField(max_length=140)
    apellido = models.CharField(max_length=140, default="")
    nss = models.CharField("NSS", max_length=30,
                           default="", validators=[validate_nss])
    email = models.CharField(max_length=140, blank=True, null=True)
    telefono_casa = models.CharField(
        'Teléfono de casa', max_length=20, blank=True, null=True)
    telefono_movil = models.CharField('Teléfono móvil', max_length=20,)
    edad = models.IntegerField(blank=True, null=True)  # choices=EDAD_CHOICES,
    curp = models.CharField("CURP", max_length=20,
                            default="", validators=[validate_curp])
    puesto = models.CharField(max_length=140)

    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, default=1)
    municipio = models.ForeignKey(
        Municipio, on_delete=models.CASCADE, default=1)

    direccion_fiscal = models.ForeignKey(
        DireccionFiscal,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name="direccion_fiscal_candidato",
        verbose_name="Dirección fiscal de facturación")

    status = models.CharField(
        max_length=140, choices=STATUS_OPCIONES, default='0')
    enviado = models.BooleanField(default=False)
    tipo_investigacion = models.ManyToManyField(ClienteTipoInvestigacion)
    sucursal = models.ForeignKey(
        Sucursales, on_delete=models.CASCADE, blank=True, null=True)

    fecha_envio = models.DateTimeField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)

    completado = models.BooleanField(default=False)

    factura_creada = models.BooleanField(default=False)
    factura_pagaga = models.BooleanField(default=False)

    archivo_solicitud = models.FileField(
        upload_to='cliente_solicitudes/', blank=True, null=True)

    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
