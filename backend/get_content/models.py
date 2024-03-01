from django.db import models
import uuid

class Animes(models.Model):
    url_img = models.TextField()
    title = models.TextField()
    descriptionEpisod = models.TextField()
    descriptionData = models.TextField()
    score = models.FloatField()

    class Meta:
        db_table = 'animes'

class Users(models.Model):
    GENDER_CHOICES = [
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
        ('Другой', 'Другой'),
    ]
        
    identifier = models.CharField(max_length=32, default=uuid.uuid4)
    name = models.TextField()
    surname = models.TextField()
    username = models.TextField()
    password = models.TextField()
    email = models.TextField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Другое')
    age = models.IntegerField(default=0)
    birthdate = models.DateField()
    photo = models.ImageField(upload_to='users_photos/', null=True, blank=True) 

    class Meta:
        db_table = 'users'


class UserProfile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True) 

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return self.user.username
    
