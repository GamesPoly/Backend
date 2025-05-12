from django.contrib import admin

from django.contrib import admin
from .models import Platform, Tag, Game

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "dev_team", "rating", "publish_date")
    list_filter = ("platforms", "tags", "dev_team")
    search_fields = ("name", "desc")
    filter_horizontal = ("tags", "platforms")
    readonly_fields = ("views", "reviews")

