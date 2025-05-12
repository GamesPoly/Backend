import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import Game

@receiver(post_delete, sender=Game)
def delete_game_files(sender, instance, **kwargs):
    for file_field in [instance.image, instance.game_file]:
        if file_field and default_storage.exists(file_field.name):
            default_storage.delete(file_field.name)
            folder = os.path.dirname(file_field.path)
            if os.path.isdir(folder) and not os.listdir(folder):
                os.rmdir(folder)
