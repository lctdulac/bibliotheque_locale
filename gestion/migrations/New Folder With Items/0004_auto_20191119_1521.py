# Generated by Django 2.2.7 on 2019-11-19 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0003_auto_20191119_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ouvrage',
            name='type',
            field=models.CharField(blank=True, choices=[('d', 'DVD'), ('v', 'Vinyl'), ('l', 'Livre'), ('c', 'CD')], help_text="Type d'ouvrage", max_length=1),
        ),
    ]
