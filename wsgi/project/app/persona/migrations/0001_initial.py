# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'File'
        db.create_table('persona_file', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('fecha_registro', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('persona', ['File'])

        # Adding model 'Persona'
        db.create_table('persona_persona', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('nss', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=140, null=True, blank=True)),
            ('edad', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('curp', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('malos_terminos', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('rfc', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('ife', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('pasaporte', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('smn', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('estado_civil', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('fecha_matrimonio', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('religion', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('tiempo_radicando', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('medio_utilizado', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('fecha_registro', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('estatus', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('persona', ['Persona'])

        # Adding model 'Telefono'
        db.create_table('persona_telefono', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('categoria', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=14, null=True, blank=True)),
            ('parentesco', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
        ))
        db.send_create_signal('persona', ['Telefono'])

        # Adding model 'Direccion'
        db.create_table('persona_direccion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('calle', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('ciudad', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('colonia', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('cp', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('estado', self.gf('django.db.models.fields.CharField')(default='Baja California', max_length=140)),
        ))
        db.send_create_signal('persona', ['Direccion'])

        # Adding model 'PrestacionVivienda'
        db.create_table('persona_prestacionvivienda', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('categoria_viv', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('activo', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('fecha_tramite', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('numero_credito', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('uso', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('persona', ['PrestacionVivienda'])

        # Adding model 'Licencia'
        db.create_table('persona_licencia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=14)),
        ))
        db.send_create_signal('persona', ['Licencia'])

        # Adding model 'Origen'
        db.create_table('persona_origen', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('lugar', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('nacionalidad', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('persona', ['Origen'])

        # Adding model 'InfoPersonal'
        db.create_table('persona_infopersonal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('objetivo_personal', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('objetivo_en_empresa', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('cualidades', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('defectos', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('trabajo_que_desarrolla', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('tatuajes', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('persona', ['InfoPersonal'])

        # Adding model 'TrayectoriaLaboral'
        db.create_table('persona_trayectorialaboral', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('compania', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['compania.Compania'])),
            ('aparece_nss', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('aportaciones_fecha_inicial', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('aportaciones_fecha_final', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('reporta_candidato', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('carta_laboral', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('carta_laboral_expide', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('puesto_inicial', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('puesto_final', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('periodo_alta', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('periodo_baja', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('sueldo_inicial', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('sueldo_final', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('funciones', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cumplio_objetivos', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('motivo_salida', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('jefe_inmediato', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('jefe_inmediato_puesto', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('no_personas_cargo', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('manejo_valores', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('recontratable', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('afiliado_sindicato', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('terminada', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('visible_en_status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('observaciones_generales', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('persona', ['TrayectoriaLaboral'])

        # Adding model 'Legalidad'
        db.create_table('persona_legalidad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('sindicato', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('afiliado_sindicato', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('demandas', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('antecedentes_penales', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('persona', ['Legalidad'])

        # Adding model 'Seguro'
        db.create_table('persona_seguro', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('ultimas_aportaciones', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('verificado_enburo', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('registro_completo', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('persona', ['Seguro'])

        # Adding model 'Salud'
        db.create_table('persona_salud', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('peso_kg', self.gf('django.db.models.fields.FloatField')()),
            ('estatura_mts', self.gf('django.db.models.fields.FloatField')()),
            ('salud_fisica', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('salud_visual', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('embarazo_meses', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ejercicio_tipo_frecuencia', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('accidentes', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('intervenciones_quirurgicas', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('enfermedades_familiares', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('tratamiento_medico_psicologico', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('enfermedades_mayor_frecuencia', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('institucion_medica', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('persona', ['Salud'])

        # Adding model 'ActividadesHabitos'
        db.create_table('persona_actividadeshabitos', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('tiempo_libre', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('extras', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('frecuencia_tabaco', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('frecuencia_alcohol', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('frecuencia_otras_sust', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('persona', ['ActividadesHabitos'])

        # Adding model 'Academica'
        db.create_table('persona_academica', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('cedula_profesional', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('cedula_prof_ano_exp', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('estudios_actuales', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('persona', ['Academica'])

        # Adding model 'GradoEscolaridad'
        db.create_table('persona_gradoescolaridad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('grado', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('institucion', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ciudad', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('anos', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('certificado', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('persona', ['GradoEscolaridad'])

        # Adding model 'OtroIdioma'
        db.create_table('persona_otroidioma', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('porcentaje', self.gf('django.db.models.fields.IntegerField')()),
            ('idioma', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('persona', ['OtroIdioma'])

        # Adding model 'SituacionVivienda'
        db.create_table('persona_situacionvivienda', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('tiempo_radicando', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tipo_mobiliario', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('sector_socioeconomico', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('personas_viven_con_evaluado', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('conservacion', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('tamano_aprox_mts2', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('persona', ['SituacionVivienda'])

        # Adding model 'PropietarioVivienda'
        db.create_table('persona_propietariovivienda', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('parentesco', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('persona', ['PropietarioVivienda'])

        # Adding model 'CaractaristicasVivienda'
        db.create_table('persona_caractaristicasvivienda', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('propia', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('rentada', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('hipotecada', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('prestada', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('otra', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('valor_aproximado', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('renta_mensual', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('persona', ['CaractaristicasVivienda'])

        # Adding model 'TipoInmueble'
        db.create_table('persona_tipoinmueble', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('casa', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('terreno_compartido', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('departamento', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('vivienda_popular', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('persona', ['TipoInmueble'])

        # Adding model 'DistribucionDimensiones'
        db.create_table('persona_distribuciondimensiones', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('habitaciones', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('banos', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('salas', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('comedor', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cocina', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('patios', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cocheras', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('persona', ['DistribucionDimensiones'])

        # Adding model 'MiembroMarcoFamiliar'
        db.create_table('persona_miembromarcofamiliar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('edad', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('ocupacion', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('empresa', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('residencia', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('persona', ['MiembroMarcoFamiliar'])

        # Adding model 'Economica'
        db.create_table('persona_economica', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('concepto', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('monto', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('persona', ['Economica'])

        # Adding model 'TarjetaCreditoComercial'
        db.create_table('persona_tarjetacreditocomercial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('institucion', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('limite_credito', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('pago_minimo', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('saldo_actual', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('persona', ['TarjetaCreditoComercial'])

        # Adding model 'CuentaDebito'
        db.create_table('persona_cuentadebito', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('institucion', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('saldo_mensual', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('antiguedad', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('ahorro', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('persona', ['CuentaDebito'])

        # Adding model 'Automovil'
        db.create_table('persona_automovil', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('marca', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('modelo_ano', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('liquidacion', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('valor_comercial', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('persona', ['Automovil'])

        # Adding model 'BienesRaices'
        db.create_table('persona_bienesraices', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('tipo_inmueble', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('ubicacion', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('liquidacion', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('valor_comercial', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('persona', ['BienesRaices'])

        # Adding model 'DeudaActual'
        db.create_table('persona_deudaactual', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('fecha_otorgamiento', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('institucion', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('cantidad_total', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('saldo_actual', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('pago_mensual', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('persona', ['DeudaActual'])

        # Adding model 'Referencia'
        db.create_table('persona_referencia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('domicilio', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('tiempo_conocido', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('parentesco', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('ocupacion', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('lugares_labor_evaluado', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('opinion', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('persona', ['Referencia'])

        # Adding model 'CuadroEvaluacion'
        db.create_table('persona_cuadroevaluacion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('conclusiones', self.gf('django.db.models.fields.TextField')()),
            ('viable', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('no_viable', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('reservas', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('persona', ['CuadroEvaluacion'])

        # Adding model 'DocumentoCotejado'
        db.create_table('persona_documentocotejado', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('estatus', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('persona', ['DocumentoCotejado'])

        # Adding model 'AspectoHogar'
        db.create_table('persona_aspectohogar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('estatus', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('persona', ['AspectoHogar'])

        # Adding model 'AspectoCandidato'
        db.create_table('persona_aspectocandidato', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('estatus', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('persona', ['AspectoCandidato'])

        # Adding model 'Evaluacion'
        db.create_table('persona_evaluacion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trayectoriaLaboral', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.TrayectoriaLaboral'])),
            ('productividad', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('adaptabilidad', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('motivacion', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('puntualidad', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('asistencia', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('disponibilidad', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('responsabilidad', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('relacion_jefe_inmediato', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('relacion_companeros', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('compromiso', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('honestidad', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('toma_decisiones', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('solucion_problemas', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('persona', ['Evaluacion'])

        # Adding model 'Opinion'
        db.create_table('persona_opinion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('evaluacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Evaluacion'])),
            ('categoria', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('opinion', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('persona', ['Opinion'])

        # Adding model 'Informante'
        db.create_table('persona_informante', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('evaluacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Evaluacion'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('puesto', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
        ))
        db.send_create_signal('persona', ['Informante'])


    def backwards(self, orm):
        # Deleting model 'File'
        db.delete_table('persona_file')

        # Deleting model 'Persona'
        db.delete_table('persona_persona')

        # Deleting model 'Telefono'
        db.delete_table('persona_telefono')

        # Deleting model 'Direccion'
        db.delete_table('persona_direccion')

        # Deleting model 'PrestacionVivienda'
        db.delete_table('persona_prestacionvivienda')

        # Deleting model 'Licencia'
        db.delete_table('persona_licencia')

        # Deleting model 'Origen'
        db.delete_table('persona_origen')

        # Deleting model 'InfoPersonal'
        db.delete_table('persona_infopersonal')

        # Deleting model 'TrayectoriaLaboral'
        db.delete_table('persona_trayectorialaboral')

        # Deleting model 'Legalidad'
        db.delete_table('persona_legalidad')

        # Deleting model 'Seguro'
        db.delete_table('persona_seguro')

        # Deleting model 'Salud'
        db.delete_table('persona_salud')

        # Deleting model 'ActividadesHabitos'
        db.delete_table('persona_actividadeshabitos')

        # Deleting model 'Academica'
        db.delete_table('persona_academica')

        # Deleting model 'GradoEscolaridad'
        db.delete_table('persona_gradoescolaridad')

        # Deleting model 'OtroIdioma'
        db.delete_table('persona_otroidioma')

        # Deleting model 'SituacionVivienda'
        db.delete_table('persona_situacionvivienda')

        # Deleting model 'PropietarioVivienda'
        db.delete_table('persona_propietariovivienda')

        # Deleting model 'CaractaristicasVivienda'
        db.delete_table('persona_caractaristicasvivienda')

        # Deleting model 'TipoInmueble'
        db.delete_table('persona_tipoinmueble')

        # Deleting model 'DistribucionDimensiones'
        db.delete_table('persona_distribuciondimensiones')

        # Deleting model 'MiembroMarcoFamiliar'
        db.delete_table('persona_miembromarcofamiliar')

        # Deleting model 'Economica'
        db.delete_table('persona_economica')

        # Deleting model 'TarjetaCreditoComercial'
        db.delete_table('persona_tarjetacreditocomercial')

        # Deleting model 'CuentaDebito'
        db.delete_table('persona_cuentadebito')

        # Deleting model 'Automovil'
        db.delete_table('persona_automovil')

        # Deleting model 'BienesRaices'
        db.delete_table('persona_bienesraices')

        # Deleting model 'DeudaActual'
        db.delete_table('persona_deudaactual')

        # Deleting model 'Referencia'
        db.delete_table('persona_referencia')

        # Deleting model 'CuadroEvaluacion'
        db.delete_table('persona_cuadroevaluacion')

        # Deleting model 'DocumentoCotejado'
        db.delete_table('persona_documentocotejado')

        # Deleting model 'AspectoHogar'
        db.delete_table('persona_aspectohogar')

        # Deleting model 'AspectoCandidato'
        db.delete_table('persona_aspectocandidato')

        # Deleting model 'Evaluacion'
        db.delete_table('persona_evaluacion')

        # Deleting model 'Opinion'
        db.delete_table('persona_opinion')

        # Deleting model 'Informante'
        db.delete_table('persona_informante')


    models = {
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
        'persona.academica': {
            'Meta': {'object_name': 'Academica'},
            'cedula_prof_ano_exp': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'cedula_profesional': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'estudios_actuales': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"})
        },
        'persona.actividadeshabitos': {
            'Meta': {'object_name': 'ActividadesHabitos'},
            'extras': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'frecuencia_alcohol': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'frecuencia_otras_sust': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'frecuencia_tabaco': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'tiempo_libre': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'persona.aspectocandidato': {
            'Meta': {'object_name': 'AspectoCandidato'},
            'estatus': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'persona.aspectohogar': {
            'Meta': {'object_name': 'AspectoHogar'},
            'estatus': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'persona.automovil': {
            'Meta': {'object_name': 'Automovil'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'liquidacion': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'marca': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'modelo_ano': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'valor_comercial': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'persona.bienesraices': {
            'Meta': {'object_name': 'BienesRaices'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'liquidacion': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'tipo_inmueble': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'ubicacion': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'valor_comercial': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'persona.caractaristicasvivienda': {
            'Meta': {'object_name': 'CaractaristicasVivienda'},
            'hipotecada': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'otra': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'prestada': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'propia': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'renta_mensual': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rentada': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'valor_aproximado': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'persona.cuadroevaluacion': {
            'Meta': {'object_name': 'CuadroEvaluacion'},
            'conclusiones': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_viable': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'reservas': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'viable': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'persona.cuentadebito': {
            'Meta': {'object_name': 'CuentaDebito'},
            'ahorro': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'antiguedad': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institucion': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'saldo_mensual': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'persona.deudaactual': {
            'Meta': {'object_name': 'DeudaActual'},
            'cantidad_total': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'fecha_otorgamiento': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institucion': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'pago_mensual': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'saldo_actual': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'persona.direccion': {
            'Meta': {'object_name': 'Direccion'},
            'calle': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'ciudad': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'colonia': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'cp': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'default': "'Baja California'", 'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"})
        },
        'persona.distribuciondimensiones': {
            'Meta': {'object_name': 'DistribucionDimensiones'},
            'banos': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'cocheras': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'cocina': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'comedor': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'habitaciones': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patios': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'salas': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'persona.documentocotejado': {
            'Meta': {'object_name': 'DocumentoCotejado'},
            'estatus': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'persona.economica': {
            'Meta': {'object_name': 'Economica'},
            'concepto': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monto': ('django.db.models.fields.FloatField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'persona.evaluacion': {
            'Meta': {'object_name': 'Evaluacion'},
            'adaptabilidad': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'asistencia': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'compromiso': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'disponibilidad': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'honestidad': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motivacion': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'productividad': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'puntualidad': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'relacion_companeros': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'relacion_jefe_inmediato': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'responsabilidad': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'solucion_problemas': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'toma_decisiones': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'trayectoriaLaboral': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.TrayectoriaLaboral']"})
        },
        'persona.file': {
            'Meta': {'object_name': 'File'},
            'fecha_registro': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'persona.gradoescolaridad': {
            'Meta': {'object_name': 'GradoEscolaridad'},
            'anos': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'certificado': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ciudad': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'grado': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institucion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"})
        },
        'persona.infopersonal': {
            'Meta': {'object_name': 'InfoPersonal'},
            'cualidades': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'defectos': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'objetivo_en_empresa': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'objetivo_personal': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'tatuajes': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'trabajo_que_desarrolla': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'persona.informante': {
            'Meta': {'object_name': 'Informante'},
            'evaluacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Evaluacion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'puesto': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        'persona.legalidad': {
            'Meta': {'object_name': 'Legalidad'},
            'afiliado_sindicato': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'antecedentes_penales': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'demandas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'sindicato': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'persona.licencia': {
            'Meta': {'object_name': 'Licencia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '14'})
        },
        'persona.miembromarcofamiliar': {
            'Meta': {'object_name': 'MiembroMarcoFamiliar'},
            'edad': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'empresa': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'ocupacion': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'residencia': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'persona.opinion': {
            'Meta': {'object_name': 'Opinion'},
            'categoria': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'evaluacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Evaluacion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opinion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'persona.origen': {
            'Meta': {'object_name': 'Origen'},
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugar': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'nacionalidad': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"})
        },
        'persona.otroidioma': {
            'Meta': {'object_name': 'OtroIdioma'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idioma': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'porcentaje': ('django.db.models.fields.IntegerField', [], {})
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
        },
        'persona.prestacionvivienda': {
            'Meta': {'object_name': 'PrestacionVivienda'},
            'activo': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'categoria_viv': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'fecha_tramite': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_credito': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'uso': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'persona.propietariovivienda': {
            'Meta': {'object_name': 'PropietarioVivienda'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parentesco': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"})
        },
        'persona.referencia': {
            'Meta': {'object_name': 'Referencia'},
            'domicilio': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugares_labor_evaluado': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'ocupacion': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'opinion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parentesco': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'tiempo_conocido': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'persona.salud': {
            'Meta': {'object_name': 'Salud'},
            'accidentes': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ejercicio_tipo_frecuencia': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'embarazo_meses': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'enfermedades_familiares': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'enfermedades_mayor_frecuencia': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'estatura_mts': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institucion_medica': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'intervenciones_quirurgicas': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'peso_kg': ('django.db.models.fields.FloatField', [], {}),
            'salud_fisica': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'salud_visual': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tratamiento_medico_psicologico': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'persona.seguro': {
            'Meta': {'object_name': 'Seguro'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'registro_completo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ultimas_aportaciones': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'verificado_enburo': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'persona.situacionvivienda': {
            'Meta': {'object_name': 'SituacionVivienda'},
            'conservacion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'personas_viven_con_evaluado': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sector_socioeconomico': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tamano_aprox_mts2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tiempo_radicando': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tipo_mobiliario': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'persona.tarjetacreditocomercial': {
            'Meta': {'object_name': 'TarjetaCreditoComercial'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institucion': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'limite_credito': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'pago_minimo': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'saldo_actual': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'persona.telefono': {
            'Meta': {'object_name': 'Telefono'},
            'categoria': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'}),
            'parentesco': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"})
        },
        'persona.tipoinmueble': {
            'Meta': {'object_name': 'TipoInmueble'},
            'casa': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'departamento': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'terreno_compartido': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vivienda_popular': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'persona.trayectorialaboral': {
            'Meta': {'object_name': 'TrayectoriaLaboral'},
            'afiliado_sindicato': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'aparece_nss': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'aportaciones_fecha_final': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'aportaciones_fecha_inicial': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'carta_laboral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'carta_laboral_expide': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'compania': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['compania.Compania']"}),
            'cumplio_objetivos': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'funciones': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jefe_inmediato': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'jefe_inmediato_puesto': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'manejo_valores': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'motivo_salida': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'no_personas_cargo': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'observaciones_generales': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'periodo_alta': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'periodo_baja': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']"}),
            'puesto_final': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'puesto_inicial': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'recontratable': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'reporta_candidato': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sueldo_final': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'sueldo_inicial': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'terminada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'visible_en_status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['persona']