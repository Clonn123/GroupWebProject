from django.db import models

class Animes(models.Model):
    url_img = models.TextField()
    title = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = 'animes'

class Users(models.Model):
    name = models.TextField()
    surname = models.TextField()
    username = models.TextField()
    password = models.TextField()
    email = models.TextField()

    class Meta:
        db_table = 'users'

