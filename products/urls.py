#django files
from django.urls import path, include

#rest files
from rest_framework.routers import DefaultRouter


#your files
from . import views


app_name = 'products'

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'brands', views.BrandViewSet, basename='brands')
router.register(r'variation', views.VariationViewSet, basename='variation')
router.register(r'products_variation', views.ProductsVariationViewSet, basename='productsVariations')
router.register(r'cart', views.CartViewSet, basename='cart')
router.register('orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),

]









