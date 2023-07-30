from django_filters import rest_framework as filters
from .models import Page


class PageFilter(filters.FilterSet):

    class Meta:
        model = Page
        fields = {
            'url': ['exact', 'contains', 'startswith'],
            'title': ['exact', 'contains', 'startswith'],
        }