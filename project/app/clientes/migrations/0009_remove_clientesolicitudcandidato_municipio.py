# Generated by Django 2.2.27 on 2022-06-15 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0008_auto_20220614_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientesolicitudcandidato',
            name='municipio',
        ),
    ]
