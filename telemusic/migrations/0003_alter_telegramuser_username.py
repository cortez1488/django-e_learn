# Generated by Django 3.2.7 on 2021-12-25 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemusic', '0002_telegramuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='username',
            field=models.CharField(max_length=75, null=True),
        ),
    ]
