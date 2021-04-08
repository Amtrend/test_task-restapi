from django_filters import rest_framework as filters

from .models import Like


class DateRangeFilterSet(filters.FilterSet):
    date_from = filters.DateFilter(field_name='put_at', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='put_at', lookup_expr='lte')

    class Meta:
        model = Like
        fields = ['date_from', 'date_to']

