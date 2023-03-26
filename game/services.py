from django_filters import rest_framework as filters
from .models import Game


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class GamesFilter(filters.FilterSet):
    # developer = CharFilterInFilter(field_name='developer__name', lookup_expr='in')
    developer = filters.CharFilter(field_name='developer__name', lookup_expr='icontains')
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')

    class Meta:
        model = Game
        fields = ['developer', 'genres']