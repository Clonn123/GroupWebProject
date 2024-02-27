from django.db import models

class Animes(models.Model):
    url_img = models.TextField()
    title = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = 'animes'

class Users(models.Model):
    GENDER_CHOICES = [
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
        ('other', 'Другое'),
    ]
        
    name = models.TextField()
    surname = models.TextField()
    username = models.TextField()
    password = models.TextField()
    email = models.TextField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='other')
    age = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='users_photos/', null=True, blank=True) 

    class Meta:
        db_table = 'users'


class UserProfile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True) 

    def __str__(self):
        return self.user.username
