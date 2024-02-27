from django.db import models

class Animes(models.Model):
    url_img = models.TextField()
    title = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = 'animes'

class Users(models.Model):
    GENDER_CHOICES = [
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
        ('Другой', 'Другой'),
    ]
        
    name = models.TextField()
    surname = models.TextField()
    username = models.TextField()
    password = models.TextField()
    email = models.TextField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Другое')
    age = models.IntegerField(default=0)

    class Meta:
        db_table = 'users'

