# Generated by Django 2.2.27 on 2022-07-02 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investigacion', '0013_auto_20220702_0439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investigacion',
            name='tipo_investigacion',
            field=models.ManyToManyField(to='clientes.ClienteTipoInvestigacion'),
        ),
    ]
