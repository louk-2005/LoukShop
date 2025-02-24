#django files
from django.test import SimpleTestCase
from django.urls import reverse, resolve

#your files
from products.views import (ProductViewSet,BrandViewSet,CategoryViewSet,VariationViewSet,ProductsVariationViewSet,
                            OrderViewSet,CartViewSet)

class TestUrls(SimpleTestCase):
    def test_category_url_list(self):
        url = reverse('products:categories-list')#it is for the two post and get method
        self.assertEqual(resolve(url).func.cls, CategoryViewSet)
    def test_category_url_detail(self):
        url = reverse('products:categories-detail', args=[1])
        self.assertEqual(resolve(url).func.cls, CategoryViewSet)
    def test_product_url_list(self):
        url = reverse('products:products-list')
        self.assertEqual(resolve(url).func.cls, ProductViewSet)
    def test_product_url_detail(self):
        url = reverse('products:products-detail', args=[1])
        self.assertEqual(resolve(url).func.cls, ProductViewSet)
    def test_Brands_url_list(self):
        url = reverse('products:brands-list')
        self.assertEqual(resolve(url).func.cls, BrandViewSet)
    def test_Brands_url_detail(self):
        url = reverse('products:brands-detail', args=[1])
        self.assertEqual(resolve(url).func.cls, BrandViewSet)
    def test_variations_url_list(self):
        url = reverse('products:variation-list')
        self.assertEqual(resolve(url).func.cls, VariationViewSet)
    def test_variations_url_detail(self):
        url = reverse('products:variation-detail', args=[1])
        self.assertEqual(resolve(url).func.cls, VariationViewSet)
    def test_products_variations_url_list(self):
        url = reverse('products:productsVariations-list')
        self.assertEqual(resolve(url).func.cls, ProductsVariationViewSet)
    def test_products_variations_url_detail(self):
        url = reverse('products:productsVariations-detail', args=[1])
        self.assertEqual(resolve(url).func.cls, ProductsVariationViewSet)
    def test_orders_url_list(self):
        url = reverse('products:order-list')
        self.assertEqual(resolve(url).func.cls, OrderViewSet)
    def test_orders_url_detail(self):
        url = reverse('products:order-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, OrderViewSet)
    def test_carts_url_list(self):
        url = reverse('products:cart-list')
        self.assertEqual(resolve(url).func.cls, CartViewSet)
    def test_carts_url_detail(self):
        url = reverse('products:cart-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, CartViewSet)
