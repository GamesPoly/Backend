
from rest_framework import generics, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Game, Platform, Tag
from .serializers import TagSerializer, PlatformSerializer, GameSerializer
from .filters import GameFilter

class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class PlatformListAPIView(generics.ListAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer

class GameListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/games/       — список игр с фильтрацией и поиском
    POST /api/games/       — создание новой игры
    """
    queryset = Game.objects.all().prefetch_related('tags','platforms')
    serializer_class = GameSerializer

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = GameFilter
    search_fields = ['name','desc']
    ordering_fields = ['publish_date','rating','views','reviews']


class GameRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/games/{pk}/   — получить игру
    PUT    /api/games/{pk}/   — полностью обновить
    PATCH  /api/games/{pk}/   — частично обновить
    DELETE /api/games/{pk}/   — удалить
    """
    queryset = Game.objects.all().prefetch_related('tags', 'platforms')
    serializer_class = GameSerializer
