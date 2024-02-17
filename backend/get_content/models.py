from django.db import models

class Animes(models.Model):
    url_img = models.TextField()
    title = models.TextField()
    description = models.TextField()
