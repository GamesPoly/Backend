from django.db import models

class Platform(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


PLAYER_MODES = [
    ('single', 'Для одного игрока'),
    ('multi', 'Мультиплеер'),
]


class Game(models.Model):
    title = models.CharField(max_length=46, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    short_description = models.CharField(max_length=300, null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)

    platforms = models.ManyToManyField(Platform)

    cpu = models.CharField(max_length=255, null=True, blank=True)
    ram = models.CharField(max_length=255, null=True, blank=True)
    gpu = models.CharField(max_length=255, null=True, blank=True)
    disk = models.CharField(max_length=255, null=True, blank=True)
    os = models.CharField(max_length=255, null=True, blank=True)
    extra_reqs = models.TextField(blank=True)

    developer_name = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)

    genres = models.ManyToManyField(Genre)
    main_genre = models.CharField(max_length=255, null=True, blank=True)

    player_mode = models.CharField(max_length=10, choices=PLAYER_MODES, null=True, blank=True)
    awards = models.TextField(blank=True)

    def __str__(self):
        return self.title