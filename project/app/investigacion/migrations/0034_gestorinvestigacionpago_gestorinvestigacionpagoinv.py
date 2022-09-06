# Generated by Django 2.2.27 on 2022-08-28 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agente', '0007_auto_20220827_0015'),
        ('investigacion', '0033_auto_20220828_0253'),
    ]

    operations = [
        migrations.CreateModel(
            name='GestorInvestigacionPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pagado', models.BooleanField(default=False)),
                ('fecha_de_pago', models.DateTimeField(blank=True, null=True)),
                ('comprobante', models.FileField(blank=True, null=True, upload_to='gestor_investigacion_pago')),
                ('created', models.DateTimeField(auto_now=True)),
                ('modificated', models.DateTimeField(auto_now_add=True)),
                ('gestor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agente.GestorInfo')),
            ],
        ),
        migrations.CreateModel(
            name='GestorInvestigacionPagoInv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gestor_investigacion_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investigacion.GestorInvestigacionPago')),
                ('investigacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investigacion.Investigacion')),
            ],
        ),
    ]
