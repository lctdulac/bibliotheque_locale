# Generated by Django 2.2.7 on 2019-11-19 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprunt',
            name='id_emprunt',
            field=models.PositiveSmallIntegerField(primary_key=True, serialize=False),
        ),
    ]
