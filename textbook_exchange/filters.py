import django_filters
from .models import ProductListing

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = ProductListing
        # fields = ['price', 'condition']
        fields = {
            'price': ['exact', 'lt'],
            'condition': ['exact'],
        }
            