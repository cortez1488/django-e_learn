# Generated by Django 3.2.7 on 2021-10-29 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Цена'),
        ),
    ]
