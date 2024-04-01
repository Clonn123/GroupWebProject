from django.db import models
import uuid

class Animes(models.Model):
    anime_list_id = models.IntegerField(primary_key=True)
    url_img = models.TextField()
    title_ru = models.TextField()
    title_en = models.TextField()
    descriptionEpisod = models.TextField()
    descriptionData = models.TextField()
    score = models.FloatField()
    studios = models.TextField()

    class Meta:
        db_table = 'animes'

class Anime_info(models.Model):
    anime_id = models.IntegerField()
    Episodes = models.IntegerField()
    Genres = models.TextField()
    Themes = models.TextField()
    
    class Meta:
        db_table = 'anime_info'

class Score(models.Model):
    REV_CHOICES = [
        ('completed', 'completed'),
        ('planned', 'planned'),
        ('dropped', 'dropped'),
        ('watching', 'watching'),
    ]
    anime_id = models.IntegerField()
    user_id = models.IntegerField()
    score = models.IntegerField()
    status = models.TextField(choices=REV_CHOICES)
    review = models.TextField()
    
    class Meta:
        db_table = 'score'

class Mangas(models.Model):
    manga_list_id = models.IntegerField(primary_key=True)
    url_img = models.TextField()
    title_ru = models.TextField()
    title_en = models.TextField()
    descriptionEpisod = models.TextField()
    descriptionData = models.TextField()
    score = models.FloatField()
    authors = models.TextField()

    class Meta:
        db_table = 'mangas'

class Manga_info(models.Model):
    manga_id = models.IntegerField()
    Episodes = models.IntegerField()
    Genres = models.TextField()
    Themes = models.TextField()
    
    class Meta:
        db_table = 'manga_info'

class Score_manga(models.Model):
    REV_CHOICES = [
        ('completed', 'completed'),
        ('planned', 'planned'),
        ('dropped', 'dropped'),
        ('watching', 'watching'),
    ]
    manga_id = models.IntegerField()
    user_id = models.IntegerField()
    score = models.IntegerField()
    status = models.TextField(choices=REV_CHOICES)
    review = models.TextField()
    
    class Meta:
        db_table = 'score_manga'

class Users(models.Model):
    GENDER_CHOICES = [
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
        ('Альтернативный', 'Альтернативный'),
    ]
    
    id = models.IntegerField(primary_key=True)
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
    
