# Generated by Django 2.2.27 on 2022-06-15 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0012_auto_20220614_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientesolicitud',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_solicitud', to='clientes.ClienteUser'),
        ),
    ]