# Generated by Django 2.2.27 on 2022-07-04 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investigacion', '0015_psicometrico_psicometricouser'),
    ]

    operations = [
        migrations.AddField(
            model_name='investigacion',
            name='entrevista_app_ejecutivo_asignado',
            field=models.BooleanField(default=False),
        ),
    ]
