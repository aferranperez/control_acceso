# Generated by Django 3.2.5 on 2021-09-29 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reconocimiento_facial', '0021_alter_raspberry_id_suscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raspberry',
            name='id_suscribe',
            field=models.CharField(editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='raspberry',
            name='ip_address',
            field=models.GenericIPAddressField(editable=False),
        ),
    ]
