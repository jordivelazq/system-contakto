# Generated by Django 2.2.27 on 2022-06-12 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_estado_municipio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipio',
            name='municipio',
            field=models.CharField(max_length=50),
        ),
    ]