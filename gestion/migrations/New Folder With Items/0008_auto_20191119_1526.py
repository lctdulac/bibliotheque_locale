# Generated by Django 2.2.7 on 2019-11-19 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0007_auto_20191119_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ouvrage',
            name='type',
            field=models.CharField(max_length=100),
        ),
    ]
