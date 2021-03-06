# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-04-12 20:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('investigacion', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cobranza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('folio', models.CharField(blank=True, default=b'', max_length=50, null=True)),
                ('status_cobranza', models.CharField(blank=True, choices=[(b'0', b'Status 1'), (b'1', b'Status 2'), (b'2', b'Pagada')], default=b'0', max_length=140, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('investigacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investigacion.Investigacion')),
            ],
        ),
    ]
