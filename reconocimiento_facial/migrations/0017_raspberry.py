# Generated by Django 3.2.5 on 2021-09-23 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reconocimiento_facial', '0016_auto_20210922_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Raspberry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('ubicacion', models.CharField(choices=[('Entrada', 'Entrada'), ('Comedor', 'Comedor'), ('Taller', 'Taller')], max_length=50)),
                ('is_active', models.BooleanField(default=False, editable=False)),
                ('is_synchronized', models.BooleanField(default=False, editable=False)),
                ('have_model', models.BooleanField(default=False, editable=False)),
                ('ip_address', models.GenericIPAddressField()),
                ('modelo', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reconocimiento_facial.modelo_entrenado')),
            ],
        ),
    ]
