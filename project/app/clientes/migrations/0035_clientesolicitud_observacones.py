# Generated by Django 2.2.27 on 2023-02-20 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0034_delete_investigacionfacturaarchivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientesolicitud',
            name='observacones',
            field=models.TextField(blank=True),
        ),
    ]