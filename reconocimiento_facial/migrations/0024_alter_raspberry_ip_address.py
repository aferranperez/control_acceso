# Generated by Django 3.2.5 on 2021-09-29 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reconocimiento_facial', '0023_alter_raspberry_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raspberry',
            name='ip_address',
            field=models.GenericIPAddressField(),
        ),
    ]
