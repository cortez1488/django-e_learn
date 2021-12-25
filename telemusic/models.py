from django.db import models

# Create your models here.

class Music(models.Model):
    name = models.CharField(max_length=75)
    path = models.FilePathField()


class TelegramUser(models.Model):
    first_name = models.CharField(max_length=75)
    username = models.CharField(max_length=75, null=True)
    ident_id = models.PositiveIntegerField(null=True)
    chat_id = models.IntegerField()
