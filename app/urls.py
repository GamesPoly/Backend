from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet  # Убедись, что этот импорт работает

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')

urlpatterns = [
    path('', include(router.urls)),
]
