# Generated by Django 3.2.5 on 2021-09-23 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reconocimiento_facial', '0015_auto_20210918_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miembro_del_modelo',
            name='CI',
            field=models.CharField(blank=True, editable=False, max_length=20),
        ),
        migrations.AlterField(
            model_name='modelo_entrenado',
            name='nombre',
            field=models.CharField(editable=False, max_length=50),
        ),
    ]