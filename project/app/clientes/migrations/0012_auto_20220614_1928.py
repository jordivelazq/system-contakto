# Generated by Django 2.2.27 on 2022-06-15 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0011_clienteuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clienteuser',
            options={'verbose_name': 'CLiente', 'verbose_name_plural': 'Clientes'},
        ),
        migrations.AlterField(
            model_name='clienteuser',
            name='compania',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compania.Compania'),
        ),
    ]
