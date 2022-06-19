# Generated by Django 2.2.27 on 2022-06-18 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0013_auto_20220614_1932'),
        ('investigacion', '0007_auto_20220322_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='investigacion',
            name='cliente_solicitud',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clientes.ClienteSolicitud'),
        ),
        migrations.AlterField(
            model_name='investigacion',
            name='agente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]