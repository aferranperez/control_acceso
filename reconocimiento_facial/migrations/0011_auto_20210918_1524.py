# Generated by Django 3.2.5 on 2021-09-18 21:24

from django.db import migrations, models
import reconocimiento_facial.models


class Migration(migrations.Migration):

    dependencies = [
        ('reconocimiento_facial', '0010_auto_20210906_1717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='imagenes_en_dataset',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='imagenes_sin_subir',
        ),
        migrations.AlterField(
            model_name='imagen',
            name='image',
            field=models.ImageField(upload_to=reconocimiento_facial.models.Imagen.persona_directory_path),
        ),
    ]
