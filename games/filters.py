import django_filters
from .models import Game

class GameFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__name', label='Tag name (in)')
    platforms = django_filters.AllValuesMultipleFilter(field_name='platforms__name', label='Platform name (in)')
    dev_team = django_filters.CharFilter(lookup_expr='exact')
    publish_date__gte = django_filters.DateFilter(field_name='publish_date', lookup_expr='gte')
    publish_date__lte = django_filters.DateFilter(field_name='publish_date', lookup_expr='lte')

    class Meta:
        model = Game
        fields = []