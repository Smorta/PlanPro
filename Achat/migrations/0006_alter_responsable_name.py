# Generated by Django 3.2 on 2021-04-22 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Achat', '0005_auto_20210415_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsable',
            name='Name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
