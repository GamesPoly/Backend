import os
from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from .validators import validate_file_size 

class Platform(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



def game_file_upload_to(instance, filename):
    team_slug = slugify(instance.dev_team or "unknown")
    return os.path.join("games-store", team_slug, filename)

class Game(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True, related_name="games")
    dev_team = models.CharField(max_length=100)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0.0)
    views = models.PositiveIntegerField(default=0)
    reviews = models.PositiveIntegerField(default=0)
    publish_date = models.DateField()
    platforms = models.ManyToManyField('Platform', related_name="games")
    
    image = models.ImageField(upload_to=game_file_upload_to, validators=[FileExtensionValidator(['jpg','jpeg','png'])])
    game_file = models.FileField(upload_to=game_file_upload_to, validators=[FileExtensionValidator(['zip','exe','apk','rar']), validate_file_size])

    def __str__(self):
        return self.name