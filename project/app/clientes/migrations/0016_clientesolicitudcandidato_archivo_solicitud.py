# Generated by Django 2.2.27 on 2022-06-21 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0015_auto_20220618_0802'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientesolicitudcandidato',
            name='archivo_solicitud',
            field=models.FileField(blank=True, null=True, upload_to='cliente_solicitudes/'),
        ),
    ]