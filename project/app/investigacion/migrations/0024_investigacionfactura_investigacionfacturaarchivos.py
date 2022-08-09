# Generated by Django 2.2.27 on 2022-08-08 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investigacion', '0023_investigacion_cliente_solicitud_candidato'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestigacionFacturaArchivos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo_pdf', models.FileField(blank=True, null=True, upload_to='archivo_factura/pdf/')),
                ('archivo_xml', models.FileField(blank=True, null=True, upload_to='archivo_factura/pdf/')),
                ('created', models.DateTimeField(auto_now=True)),
                ('modificated', models.DateTimeField(auto_now_add=True)),
                ('investigacion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='investigacion_factura_archivos', to='investigacion.Investigacion')),
            ],
        ),
        migrations.CreateModel(
            name='InvestigacionFactura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveSmallIntegerField(default=0)),
                ('descripcion', models.CharField(max_length=140)),
                ('monto', models.FloatField(default=0)),
                ('descuento', models.FloatField(default=0)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('investigacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investigacion_factura', to='investigacion.Investigacion')),
            ],
        ),
    ]
