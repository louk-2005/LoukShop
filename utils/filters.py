#djago files
import django_filters

#your file
from products.models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields={
            'title': ['exact', 'icontains','startswith'],
            'price':['exact','lt','gt','lte','gte'],
            'is_active':['exact'],
        }





