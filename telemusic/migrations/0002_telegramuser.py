# Generated by Django 3.2.7 on 2021-12-25 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemusic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=75)),
                ('username', models.CharField(max_length=75)),
                ('chat_id', models.IntegerField()),
            ],
        ),
    ]
