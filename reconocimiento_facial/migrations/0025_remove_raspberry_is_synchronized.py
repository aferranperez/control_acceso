# Generated by Django 3.2.5 on 2021-09-30 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reconocimiento_facial', '0024_alter_raspberry_ip_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='raspberry',
            name='is_synchronized',
        ),
    ]
