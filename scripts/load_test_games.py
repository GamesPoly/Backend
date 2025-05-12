from games.models import Game, Tag, Platform
from django.core.files.base import ContentFile
from django.utils import timezone
import tempfile

# Создание платформ
platforms = ['Windows', 'Android', 'iOS','MacOS']
platform_objs = [Platform.objects.get_or_create(name=name)[0] for name in platforms]

# Создание тегов
tags = ['Экшен', 'Приключения', 'Ролевая игра', 'Стратегия', 'Шутер', 'Головоломка', 'Платформер', 'Хоррор', 'Симулятор', 'Спорт', 'Гонки', 'Файтинг', 'Стелс', 'Выживание', 'Рогалик', 'Визуальная новелла', 'Песочница', 'MOBA', 'MMORPG', 'Карточная игра']
tag_objs = [Tag.objects.get_or_create(name=name)[0] for name in tags]

# Фейковые файлы
image = ContentFile(b'\x47\x49\x46', name='fake.png')  # GIF заглушка
game_file = ContentFile(b'Fake game binary', name='game.zip')

# Создание игры
game, created = Game.objects.get_or_create(
    name='Test Game',
    defaults={
        'desc': 'A test game description.',
        'dev_team': 'TestDevTeam',
        'rating': 4.5,
        'views': 123,
        'reviews': 10,
        'publish_date': timezone.now().date(),
        'image': image,
        'game_file': game_file,
    }
)
if created:
    game.platforms.set(platform_objs)
    game.tags.set(tag_objs)
    print("Test game created.")
else:
    print("Test game already exists.")
