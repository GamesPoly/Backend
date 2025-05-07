from django.urls import path
from .views import GameListCreateAPIView, GameRetrieveUpdateDestroyAPIView, TagListAPIView, PlatformListAPIView

urlpatterns = [
    path('',GameListCreateAPIView.as_view(),name='game-list-create'),
    path('<int:pk>/',GameRetrieveUpdateDestroyAPIView.as_view(),name='game-detail'),
    path('tags/', TagListAPIView.as_view(), name='tag-list'),
    path('platforms/', PlatformListAPIView.as_view(), name='platform-list'),
]