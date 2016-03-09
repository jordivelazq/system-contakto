# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EntrevistaFile'
        db.create_table('entrevista_entrevistafile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('fecha_registro', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaFile'])

        # Adding model 'EntrevistaPersona'
        db.create_table('entrevista_entrevistapersona', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('investigacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['investigacion.Investigacion'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('nss', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('edad', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('curp', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('rfc', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('ife', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('pasaporte', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('smn', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('estado_civil', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('fecha_matrimonio', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('religion', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('tiempo_radicando', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('medio_utilizado', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('fecha_registro', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('activa', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('dependientes_economicos', self.gf('django.db.models.fields.TextField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaPersona'])

        # Adding model 'EntrevistaInvestigacion'
        db.create_table('entrevista_entrevistainvestigacion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('empresa_contratante', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('fecha_recibido', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('puesto', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('fecha_registro', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('conclusiones', self.gf('django.db.models.fields.TextField')()),
            ('resultado', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('archivo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaFile'], null=True, blank=True)),
            ('folio', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('presupuesto', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaInvestigacion'])

        # Adding model 'EntrevistaCita'
        db.create_table('entrevista_entrevistacita', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('investigacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['investigacion.Investigacion'])),
            ('fecha_entrevista', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('hora_entrevista', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('entrevistador', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('autorizada', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('observaciones', self.gf('django.db.models.fields.TextField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaCita'])

        # Adding model 'EntrevistaTelefono'
        db.create_table('entrevista_entrevistatelefono', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('categoria', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('parentesco', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaTelefono'])

        # Adding model 'EntrevistaDireccion'
        db.create_table('entrevista_entrevistadireccion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('calle', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('ciudad', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('colonia', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('cp', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('estado', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaDireccion'])

        # Adding model 'EntrevistaPrestacionVivienda'
        db.create_table('entrevista_entrevistaprestacionvivienda', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('categoria_viv', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('activo', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('fecha_tramite', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('numero_credito', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('uso', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaPrestacionVivienda'])

        # Adding model 'EntrevistaLicencia'
        db.create_table('entrevista_entrevistalicencia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=14, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaLicencia'])

        # Adding model 'EntrevistaOrigen'
        db.create_table('entrevista_entrevistaorigen', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('lugar', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('nacionalidad', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaOrigen'])

        # Adding model 'EntrevistaInfoPersonal'
        db.create_table('entrevista_entrevistainfopersonal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('objetivo_personal', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('objetivo_en_empresa', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('cualidades', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('defectos', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('trabajo_que_desarrolla', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('antecedentes_penales', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('tatuajes', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaInfoPersonal'])

        # Adding model 'EntrevistaHistorialEnEmpresa'
        db.create_table('entrevista_entrevistahistorialenempresa', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('categoria', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tiene', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('puesto', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('periodo', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaHistorialEnEmpresa'])

        # Adding model 'EntrevistaSalud'
        db.create_table('entrevista_entrevistasalud', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('peso_kg', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('estatura_mts', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('salud_fisica', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('salud_visual', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('embarazo_meses', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('ejercicio_tipo_frecuencia', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('accidentes', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('intervenciones_quirurgicas', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('enfermedades_familiares', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('tratamiento_medico_psicologico', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('enfermedades_mayor_frecuencia', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('institucion_medica', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaSalud'])

        # Adding model 'EntrevistaActividadesHabitos'
        db.create_table('entrevista_entrevistaactividadeshabitos', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('tiempo_libre', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('extras', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('frecuencia_tabaco', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('frecuencia_alcohol', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('frecuencia_otras_sust', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaActividadesHabitos'])

        # Adding model 'EntrevistaAcademica'
        db.create_table('entrevista_entrevistaacademica', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('cedula_profesional', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('cedula_prof_ano_exp', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('estudios_actuales', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaAcademica'])

        # Adding model 'EntrevistaGradoEscolaridad'
        db.create_table('entrevista_entrevistagradoescolaridad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('grado', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('institucion', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('ciudad', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('anos', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('certificado', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaGradoEscolaridad'])

        # Adding model 'EntrevistaOtroIdioma'
        db.create_table('entrevista_entrevistaotroidioma', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('porcentaje', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('idioma', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaOtroIdioma'])

        # Adding model 'EntrevistaSituacionVivienda'
        db.create_table('entrevista_entrevistasituacionvivienda', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('tiempo_radicando', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('tipo_mobiliario', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('sector_socioeconomico', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('personas_viven_con_evaluado', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('conservacion', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('tamano_aprox_mts2', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaSituacionVivienda'])

        # Adding model 'EntrevistaPropietarioVivienda'
        db.create_table('entrevista_entrevistapropietariovivienda', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('parentesco', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaPropietarioVivienda'])

        # Adding model 'EntrevistaCaractaristicasVivienda'
        db.create_table('entrevista_entrevistacaractaristicasvivienda', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('propia', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('rentada', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('hipotecada', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('prestada', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('otra', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('valor_aproximado', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('renta_mensual', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaCaractaristicasVivienda'])

        # Adding model 'EntrevistaTipoInmueble'
        db.create_table('entrevista_entrevistatipoinmueble', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('casa', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('terreno_compartido', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('departamento', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('vivienda_popular', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('otro_tipo', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaTipoInmueble'])

        # Adding model 'EntrevistaDistribucionDimensiones'
        db.create_table('entrevista_entrevistadistribuciondimensiones', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('habitaciones', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('banos', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('salas', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('comedor', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('cocina', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('patios', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('cocheras', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaDistribucionDimensiones'])

        # Adding model 'EntrevistaMiembroMarcoFamiliar'
        db.create_table('entrevista_entrevistamiembromarcofamiliar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('edad', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('ocupacion', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('empresa', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('residencia', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaMiembroMarcoFamiliar'])

        # Adding model 'EntrevistaEconomica'
        db.create_table('entrevista_entrevistaeconomica', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('concepto', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('monto', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaEconomica'])

        # Adding model 'EntrevistaTarjetaCreditoComercial'
        db.create_table('entrevista_entrevistatarjetacreditocomercial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('institucion', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('limite_credito', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('pago_minimo', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('saldo_actual', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaTarjetaCreditoComercial'])

        # Adding model 'EntrevistaCuentaDebito'
        db.create_table('entrevista_entrevistacuentadebito', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('institucion', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('saldo_mensual', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('antiguedad', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('ahorro', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaCuentaDebito'])

        # Adding model 'EntrevistaAutomovil'
        db.create_table('entrevista_entrevistaautomovil', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('marca', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('modelo_ano', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('liquidacion', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('valor_comercial', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaAutomovil'])

        # Adding model 'EntrevistaBienesRaices'
        db.create_table('entrevista_entrevistabienesraices', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('tipo_inmueble', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('ubicacion', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('liquidacion', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('valor_comercial', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaBienesRaices'])

        # Adding model 'EntrevistaSeguro'
        db.create_table('entrevista_entrevistaseguro', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('empresa', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('forma_pago', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('vigencia', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaSeguro'])

        # Adding model 'EntrevistaDeudaActual'
        db.create_table('entrevista_entrevistadeudaactual', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('fecha_otorgamiento', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('institucion', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('cantidad_total', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('saldo_actual', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('pago_mensual', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaDeudaActual'])

        # Adding model 'EntrevistaReferencia'
        db.create_table('entrevista_entrevistareferencia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('domicilio', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('tiempo_conocido', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('parentesco', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('ocupacion', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('lugares_labor_evaluado', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('opinion', self.gf('django.db.models.fields.TextField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaReferencia'])

        # Adding model 'EntrevistaDocumentoCotejado'
        db.create_table('entrevista_entrevistadocumentocotejado', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('estatus', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('observaciones', self.gf('django.db.models.fields.TextField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaDocumentoCotejado'])

        # Adding model 'EntrevistaAspectoHogar'
        db.create_table('entrevista_entrevistaaspectohogar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('estatus', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaAspectoHogar'])

        # Adding model 'EntrevistaAspectoCandidato'
        db.create_table('entrevista_entrevistaaspectocandidato', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entrevista.EntrevistaPersona'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('estatus', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('entrevista', ['EntrevistaAspectoCandidato'])


    def backwards(self, orm):
        # Deleting model 'EntrevistaFile'
        db.delete_table('entrevista_entrevistafile')

        # Deleting model 'EntrevistaPersona'
        db.delete_table('entrevista_entrevistapersona')

        # Deleting model 'EntrevistaInvestigacion'
        db.delete_table('entrevista_entrevistainvestigacion')

        # Deleting model 'EntrevistaCita'
        db.delete_table('entrevista_entrevistacita')

        # Deleting model 'EntrevistaTelefono'
        db.delete_table('entrevista_entrevistatelefono')

        # Deleting model 'EntrevistaDireccion'
        db.delete_table('entrevista_entrevistadireccion')

        # Deleting model 'EntrevistaPrestacionVivienda'
        db.delete_table('entrevista_entrevistaprestacionvivienda')

        # Deleting model 'EntrevistaLicencia'
        db.delete_table('entrevista_entrevistalicencia')

        # Deleting model 'EntrevistaOrigen'
        db.delete_table('entrevista_entrevistaorigen')

        # Deleting model 'EntrevistaInfoPersonal'
        db.delete_table('entrevista_entrevistainfopersonal')

        # Deleting model 'EntrevistaHistorialEnEmpresa'
        db.delete_table('entrevista_entrevistahistorialenempresa')

        # Deleting model 'EntrevistaSalud'
        db.delete_table('entrevista_entrevistasalud')

        # Deleting model 'EntrevistaActividadesHabitos'
        db.delete_table('entrevista_entrevistaactividadeshabitos')

        # Deleting model 'EntrevistaAcademica'
        db.delete_table('entrevista_entrevistaacademica')

        # Deleting model 'EntrevistaGradoEscolaridad'
        db.delete_table('entrevista_entrevistagradoescolaridad')

        # Deleting model 'EntrevistaOtroIdioma'
        db.delete_table('entrevista_entrevistaotroidioma')

        # Deleting model 'EntrevistaSituacionVivienda'
        db.delete_table('entrevista_entrevistasituacionvivienda')

        # Deleting model 'EntrevistaPropietarioVivienda'
        db.delete_table('entrevista_entrevistapropietariovivienda')

        # Deleting model 'EntrevistaCaractaristicasVivienda'
        db.delete_table('entrevista_entrevistacaractaristicasvivienda')

        # Deleting model 'EntrevistaTipoInmueble'
        db.delete_table('entrevista_entrevistatipoinmueble')

        # Deleting model 'EntrevistaDistribucionDimensiones'
        db.delete_table('entrevista_entrevistadistribuciondimensiones')

        # Deleting model 'EntrevistaMiembroMarcoFamiliar'
        db.delete_table('entrevista_entrevistamiembromarcofamiliar')

        # Deleting model 'EntrevistaEconomica'
        db.delete_table('entrevista_entrevistaeconomica')

        # Deleting model 'EntrevistaTarjetaCreditoComercial'
        db.delete_table('entrevista_entrevistatarjetacreditocomercial')

        # Deleting model 'EntrevistaCuentaDebito'
        db.delete_table('entrevista_entrevistacuentadebito')

        # Deleting model 'EntrevistaAutomovil'
        db.delete_table('entrevista_entrevistaautomovil')

        # Deleting model 'EntrevistaBienesRaices'
        db.delete_table('entrevista_entrevistabienesraices')

        # Deleting model 'EntrevistaSeguro'
        db.delete_table('entrevista_entrevistaseguro')

        # Deleting model 'EntrevistaDeudaActual'
        db.delete_table('entrevista_entrevistadeudaactual')

        # Deleting model 'EntrevistaReferencia'
        db.delete_table('entrevista_entrevistareferencia')

        # Deleting model 'EntrevistaDocumentoCotejado'
        db.delete_table('entrevista_entrevistadocumentocotejado')

        # Deleting model 'EntrevistaAspectoHogar'
        db.delete_table('entrevista_entrevistaaspectohogar')

        # Deleting model 'EntrevistaAspectoCandidato'
        db.delete_table('entrevista_entrevistaaspectocandidato')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'compania.compania': {
            'Meta': {'object_name': 'Compania'},
            'ciudad': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'es_cliente': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha_creacion': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'notas': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'razon_social': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'referencia_correo': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'rfc': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'rfc_direccion': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sucursal': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'telefono_alt': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'compania.contacto': {
            'Meta': {'object_name': 'Contacto'},
            'compania': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'compania_contacto'", 'to': "orm['compania.Compania']"}),
            'costo_inv_completa': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'costo_inv_laboral': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '250'}),
            'email_alt': ('django.db.models.fields.EmailField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'puesto': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'telefono_celular': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'telefono_otro': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'entrevista.entrevistaacademica': {
            'Meta': {'object_name': 'EntrevistaAcademica'},
            'cedula_prof_ano_exp': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'cedula_profesional': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'estudios_actuales': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"})
        },
        'entrevista.entrevistaactividadeshabitos': {
            'Meta': {'object_name': 'EntrevistaActividadesHabitos'},
            'extras': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'frecuencia_alcohol': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'frecuencia_otras_sust': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'frecuencia_tabaco': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'tiempo_libre': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistaaspectocandidato': {
            'Meta': {'object_name': 'EntrevistaAspectoCandidato'},
            'estatus': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'entrevista.entrevistaaspectohogar': {
            'Meta': {'object_name': 'EntrevistaAspectoHogar'},
            'estatus': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'entrevista.entrevistaautomovil': {
            'Meta': {'object_name': 'EntrevistaAutomovil'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'liquidacion': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'marca': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'modelo_ano': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'valor_comercial': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistabienesraices': {
            'Meta': {'object_name': 'EntrevistaBienesRaices'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'liquidacion': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'tipo_inmueble': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'ubicacion': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'valor_comercial': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistacaractaristicasvivienda': {
            'Meta': {'object_name': 'EntrevistaCaractaristicasVivienda'},
            'hipotecada': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'otra': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'prestada': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'propia': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'renta_mensual': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'rentada': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'valor_aproximado': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistacita': {
            'Meta': {'object_name': 'EntrevistaCita'},
            'autorizada': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'entrevistador': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'fecha_entrevista': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hora_entrevista': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investigacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['investigacion.Investigacion']"}),
            'observaciones': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistacuentadebito': {
            'Meta': {'object_name': 'EntrevistaCuentaDebito'},
            'ahorro': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'antiguedad': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institucion': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'saldo_mensual': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistadeudaactual': {
            'Meta': {'object_name': 'EntrevistaDeudaActual'},
            'cantidad_total': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'fecha_otorgamiento': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institucion': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'pago_mensual': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'saldo_actual': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistadireccion': {
            'Meta': {'object_name': 'EntrevistaDireccion'},
            'calle': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'ciudad': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'colonia': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'cp': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"})
        },
        'entrevista.entrevistadistribuciondimensiones': {
            'Meta': {'object_name': 'EntrevistaDistribucionDimensiones'},
            'banos': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cocheras': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cocina': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'comedor': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'habitaciones': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patios': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'salas': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistadocumentocotejado': {
            'Meta': {'object_name': 'EntrevistaDocumentoCotejado'},
            'estatus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observaciones': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'entrevista.entrevistaeconomica': {
            'Meta': {'object_name': 'EntrevistaEconomica'},
            'concepto': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monto': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'entrevista.entrevistafile': {
            'Meta': {'object_name': 'EntrevistaFile'},
            'fecha_registro': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'entrevista.entrevistagradoescolaridad': {
            'Meta': {'object_name': 'EntrevistaGradoEscolaridad'},
            'anos': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'certificado': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ciudad': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'grado': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institucion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"})
        },
        'entrevista.entrevistahistorialenempresa': {
            'Meta': {'object_name': 'EntrevistaHistorialEnEmpresa'},
            'categoria': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'periodo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'puesto': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'tiene': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistainfopersonal': {
            'Meta': {'object_name': 'EntrevistaInfoPersonal'},
            'antecedentes_penales': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'cualidades': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'defectos': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'objetivo_en_empresa': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'objetivo_personal': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'tatuajes': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'trabajo_que_desarrolla': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistainvestigacion': {
            'Meta': {'object_name': 'EntrevistaInvestigacion'},
            'agente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'archivo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaFile']", 'null': 'True', 'blank': 'True'}),
            'conclusiones': ('django.db.models.fields.TextField', [], {}),
            'empresa_contratante': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'fecha_recibido': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'fecha_registro': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'folio': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'presupuesto': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'puesto': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'resultado': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistalicencia': {
            'Meta': {'object_name': 'EntrevistaLicencia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistamiembromarcofamiliar': {
            'Meta': {'object_name': 'EntrevistaMiembroMarcoFamiliar'},
            'edad': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'empresa': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'ocupacion': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'residencia': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'entrevista.entrevistaorigen': {
            'Meta': {'object_name': 'EntrevistaOrigen'},
            'fecha': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugar': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'nacionalidad': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"})
        },
        'entrevista.entrevistaotroidioma': {
            'Meta': {'object_name': 'EntrevistaOtroIdioma'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idioma': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'porcentaje': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistapersona': {
            'Meta': {'object_name': 'EntrevistaPersona'},
            'activa': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'curp': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'dependientes_economicos': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'edad': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'estado_civil': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fecha_matrimonio': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fecha_registro': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ife': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'investigacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['investigacion.Investigacion']"}),
            'medio_utilizado': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'nss': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'pasaporte': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'religion': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'rfc': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'smn': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'tiempo_radicando': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistaprestacionvivienda': {
            'Meta': {'object_name': 'EntrevistaPrestacionVivienda'},
            'activo': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'categoria_viv': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'fecha_tramite': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_credito': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'uso': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistapropietariovivienda': {
            'Meta': {'object_name': 'EntrevistaPropietarioVivienda'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'parentesco': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"})
        },
        'entrevista.entrevistareferencia': {
            'Meta': {'object_name': 'EntrevistaReferencia'},
            'domicilio': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugares_labor_evaluado': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'ocupacion': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'opinion': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'parentesco': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'tiempo_conocido': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistasalud': {
            'Meta': {'object_name': 'EntrevistaSalud'},
            'accidentes': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ejercicio_tipo_frecuencia': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'embarazo_meses': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'enfermedades_familiares': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'enfermedades_mayor_frecuencia': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'estatura_mts': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institucion_medica': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'intervenciones_quirurgicas': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'peso_kg': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'salud_fisica': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'salud_visual': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tratamiento_medico_psicologico': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistaseguro': {
            'Meta': {'object_name': 'EntrevistaSeguro'},
            'empresa': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'forma_pago': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'vigencia': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistasituacionvivienda': {
            'Meta': {'object_name': 'EntrevistaSituacionVivienda'},
            'conservacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'personas_viven_con_evaluado': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sector_socioeconomico': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tamano_aprox_mts2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tiempo_radicando': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tipo_mobiliario': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistatarjetacreditocomercial': {
            'Meta': {'object_name': 'EntrevistaTarjetaCreditoComercial'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institucion': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'limite_credito': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'pago_minimo': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'saldo_actual': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        'entrevista.entrevistatelefono': {
            'Meta': {'object_name': 'EntrevistaTelefono'},
            'categoria': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'parentesco': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"})
        },
        'entrevista.entrevistatipoinmueble': {
            'Meta': {'object_name': 'EntrevistaTipoInmueble'},
            'casa': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'otro_tipo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entrevista.EntrevistaPersona']"}),
            'terreno_compartido': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'vivienda_popular': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'investigacion.investigacion': {
            'Meta': {'object_name': 'Investigacion'},
            'agente': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'archivo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.File']", 'null': 'True', 'blank': 'True'}),
            'candidato': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'compania': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['compania.Compania']"}),
            'conclusiones': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contacto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['compania.Contacto']"}),
            'entrevista': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'familiar_laborando': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'fecha_recibido': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_registro': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'folio': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'laboro_anteriormente': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'observaciones': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'observaciones_generales': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'presupuesto': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'puesto': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'resultado': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'status_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status_general': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'tipo_investigacion_status': ('django.db.models.fields.IntegerField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'tipo_investigacion_texto': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'persona.file': {
            'Meta': {'object_name': 'File'},
            'fecha_registro': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'persona.persona': {
            'Meta': {'object_name': 'Persona'},
            'curp': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'edad': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'estado_civil': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'estatus': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fecha_matrimonio': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_registro': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ife': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'malos_terminos': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'medio_utilizado': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'nss': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'pasaporte': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'religion': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'rfc': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'smn': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'tiempo_radicando': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['entrevista']