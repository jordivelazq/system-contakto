# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2021-05-05 02:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adjuntos', '0002_auto_20201004_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='adjuntos',
            name='adj36',
            field=models.FileField(blank=True, null=True, upload_to='adj', verbose_name='Validacion web'),
        ),
    ]