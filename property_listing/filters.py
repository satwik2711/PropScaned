# filters.py
import django_filters
from .models import PropertyType1, PropertyType2, PropertyType3
import django_filters

class PropertyType1Filter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
    locality = django_filters.CharFilter(field_name="locality", lookup_expr='icontains')
    locality_society = django_filters.CharFilter(field_name="locality_society", lookup_expr='icontains')
    sub_locality = django_filters.CharFilter(field_name="sub_locality", lookup_expr='icontains')
    id = django_filters.NumberFilter(field_name="id", lookup_expr="exact")
    listing_type = django_filters.CharFilter(field_name="listing_type", lookup_expr='icontains')

    class Meta:
        model = PropertyType1
        fields = {
            'id': ['exact'],
            'city': ['exact', 'icontains'],
            'listing_type': ['exact', 'icontains'],
            'user': ['exact'],
            'locality': ['exact', 'icontains'],
            'locality_society': ['exact', 'icontains'],
            'sub_locality': ['exact', 'icontains'],
        }

class PropertyType2Filter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
    locality = django_filters.CharFilter(field_name="locality", lookup_expr='icontains')
    locality_society = django_filters.CharFilter(field_name="locality_society", lookup_expr='icontains')
    sub_locality = django_filters.CharFilter(field_name="sub_locality", lookup_expr='icontains')
    id = django_filters.NumberFilter(field_name="id", lookup_expr="exact")
    listing_type = django_filters.CharFilter(field_name="listing_type", lookup_expr='icontains')

    class Meta:
        model = PropertyType2
        fields = {
            'id': ['exact'],
            'city': ['exact', 'icontains'],
            'listing_type': ['exact', 'icontains'],
            'user': ['exact'],
            'locality': ['exact', 'icontains'],
            'locality_society': ['exact', 'icontains'],
            'sub_locality': ['exact', 'icontains'],
        }

class PropertyType3Filter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
    locality = django_filters.CharFilter(field_name="locality", lookup_expr='icontains')
    locality_society = django_filters.CharFilter(field_name="locality_society", lookup_expr='icontains')
    sub_locality = django_filters.CharFilter(field_name="sub_locality", lookup_expr='icontains')
    id = django_filters.NumberFilter(field_name="id", lookup_expr="exact")
    listing_type = django_filters.CharFilter(field_name="listing_type", lookup_expr='icontains')
    
    class Meta:
        model = PropertyType3
        fields = {
            'id': ['exact'],
            'city': ['exact', 'icontains'],
            'listing_type': ['exact', 'icontains'],
            'user': ['exact'],
            'locality': ['exact', 'icontains'],
            'locality_society': ['exact', 'icontains'],
            'sub_locality': ['exact', 'icontains'],
        }
