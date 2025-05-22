from datetime import date
from django.utils.text import slugify
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from rest_framework import serializers
from .models import Game, Tag, Platform

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name']

class GameSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )
    platforms = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Platform.objects.all()
    )

    # Не обязательные поля при редактировании игры, чтобы не загружать повторно
    image = serializers.ImageField(required=False)
    game_file = serializers.FileField(required=False)

    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ('id', 'views', 'reviews', 'rating')

    def validate_publish_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Дата публикации не может быть в будущем")
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        platforms = validated_data.pop('platforms', [])
        image = validated_data.pop('image', None)
        game_file = validated_data.pop('game_file', None)

        instance = Game.objects.create(**validated_data)

        team_slug = slugify(instance.dev_team or 'unknown')

        if image:
            image_path = f"games-store/{team_slug}/{image.name}"
            saved_path = default_storage.save(image_path, ContentFile(image.read()))
            instance.image.name = saved_path

        if game_file:
            file_path = f"games-store/{team_slug}/{game_file.name}"
            saved_path = default_storage.save(file_path, ContentFile(game_file.read()))
            instance.game_file.name = saved_path

        instance.save()
        instance.tags.set(tags)
        instance.platforms.set(platforms)

        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        platforms = validated_data.pop('platforms', None)
        image = validated_data.pop('image', None)
        game_file = validated_data.pop('game_file', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        team_slug = slugify(instance.dev_team or 'unknown')

        # При обновлении - image необязательное поле
        if image is not None:
            if image:
                if instance.image and default_storage.exists(instance.image.name):
                    default_storage.delete(instance.image.name)
                image_path = f"games-store/{team_slug}/{image.name}"
                saved_path = default_storage.save(image_path, ContentFile(image.read()))
                instance.image.name = saved_path
            else:
                # Если явно передан null или пустое значение - удалить файл
                if instance.image and default_storage.exists(instance.image.name):
                    default_storage.delete(instance.image.name)
                instance.image = None

        # Аналогично для game_file
        if game_file is not None:
            if game_file:
                if instance.game_file and default_storage.exists(instance.game_file.name):
                    default_storage.delete(instance.game_file.name)
                file_path = f"games-store/{team_slug}/{game_file.name}"
                saved_path = default_storage.save(file_path, ContentFile(game_file.read()))
                instance.game_file.name = saved_path
            else:
                if instance.game_file and default_storage.exists(instance.game_file.name):
                    default_storage.delete(instance.game_file.name)
                instance.game_file = None

        instance.save()

        if tags is not None:
            instance.tags.set(tags)
        if platforms is not None:
            instance.platforms.set(platforms)

        return instance