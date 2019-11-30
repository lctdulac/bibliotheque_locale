# Generated by Django 2.2.7 on 2019-11-28 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0004_auto_20191125_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auteur',
            name='img',
            field=models.ImageField(upload_to='img/', verbose_name="Photo de l'auteur"),
        ),
        migrations.AlterField(
            model_name='ouvrage',
            name='type',
            field=models.CharField(blank=True, choices=[('r', 'Revue'), ('d', 'DVD'), ('v', 'Vinyl'), ('l', 'Livre'), ('c', 'CD')], help_text="Type d'ouvrage", max_length=1),
        ),
    ]
