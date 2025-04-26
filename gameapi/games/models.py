from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    photo_url = models.URLField(blank=True, null=True)  # Change from ImageField to URLField
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title