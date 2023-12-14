# Generated by Django 2.2.27 on 2022-08-24 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0032_auto_20220816_0401'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestigacionFacturaArchivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notas', models.TextField(blank=True, null=True)),
                ('fecha', models.DateField()),
                ('comprobante', models.FileField(blank=True, null=True, upload_to='comprobantes/pago/clientes', verbose_name='Archivo en formato PDF o JPG')),
                ('verificado_por_cobranzas', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now=True)),
                ('modificated', models.DateTimeField(auto_now_add=True)),
                ('cliente_solicitud_candidato_factura', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_solicitud_candidato_factura', to='clientes.ClienteSolicitudCandidato')),
            ],
        ),
    ]