#django files
from itertools import product

from django.test import TestCase
from django.utils import timezone
from autoslug import AutoSlugField

#special pakage
from model_bakery import baker


#your files
from products.models import Product, Category, Variation, ProductVariant, Brand, Cart, Order
from accounts.models import User
from products.serializers import (ProductSerializer, CategorySerializer, ProductVariantsSerializer,
                                  VariantSerializer, CartSerializer, OrderSerializer, CartItemSerializer,OrderAddress)
from base import settings

class CategorySerializerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(title='Test Category')

    def test_category_serializer_without_parent(self):
        form = CategorySerializer(data={'title':'test'})
        self.assertTrue(form.is_valid(), form.errors)
    def test_category_serializer_without_parent_empty_title(self):
        form = CategorySerializer(data={})
        self.assertFalse(form.is_valid(), form.errors)
        self.assertEqual(len(form.errors),1)

    def test_category_serializer_with_parent(self):
        form = CategorySerializer(data={'title':'test','parent':self.category.id})
        self.assertTrue(form.is_valid(), form.errors)
    def test_category_serializer_with_wrong_parent(self):
        form = CategorySerializer(data={'title':'test','parent':'sdf'})
        self.assertFalse(form.is_valid(), form.errors)
        self.assertEqual(len(form.errors),1)




class VariationSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.brand = Brand.objects.create(brand_name='Test Brand')
    def test_variation_serializer(self):
       form = VariantSerializer(data={'color':'red','size':'234','brands':self.brand})
       self.assertTrue(form.is_valid(), form.errors)
    def test_variation_serializer_without_data(self):
        form = VariantSerializer(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),2)

class ProductSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = baker.make(Category,slug='test',parent=None)

    def test_products_serializer(self):
        form = ProductSerializer(data={'title':'Test Product','category':self.category.id,'slug':'sdf',
                'price':234,'description':'Test Product','is_active':True}
        )
        self.assertTrue(form.is_valid(), form.errors)
    def test_products_serializer_without_title(self):
        form = ProductSerializer(data={ 'category': self.category.id, 'slug': 'sdf',
                                       'price': 234, 'description': 'Test Product', 'is_active': True}
                                 )
        self.assertFalse(form.is_valid(), form.errors)
        self.assertEqual(len(form.errors),1)
        language = getattr(settings, 'LANGUAGE_CODE')
        if language == 'en':
            self.assertIn('This field is required.', form.errors['title'])
        elif language == 'fa':
            self.assertIn('این مقدار لازم است.', form.errors['title'])
class ProductVariantsSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.variation= baker.make(Variation)
        cls.category = baker.make(Category,slug='test',parent=None)
        cls.product=baker.make(Product,slug='sdf',description='Test Product',category=cls.category)
        cls.data={'variation':cls.variation.id,'additional_price':234,'product':cls.product.id}
    def test_product_variant_serializer(self):
        form = ProductVariantsSerializer(data=self.data)
        self.assertTrue(form.is_valid(), form.errors)
    def test_product_variant_serializer_without_product(self):
        form = ProductVariantsSerializer(data={'variation':self.variation.id,'additional_price':234})
        self.assertFalse(form.is_valid(), form.errors)
        self.assertEqual(len(form.errors),1)
        language=getattr(settings, 'LANGUAGE_CODE')
        if language == 'en':
            self.assertIn('This field is required.', form.errors['product'])
        elif language == 'fa':
            self.assertIn('این مقدار لازم است.',form.errors['product'])
class CartItemSerializerTest(TestCase):

    def setUp(self):
        self.category = baker.make(Category,slug='test',parent=None)
        self.product=baker.make(Product,slug='sdf',description='Test Product',category=self.category,is_active=True,id=2)
        self.cart= baker.make(Cart)
        self.variation=baker.make(Variation)
        self.productVariant=baker.make(ProductVariant,variation=self.variation,product=self.product)
        self.data={'product_variant':self.productVariant.id,'product':self.product.id,'cart':self.cart.id,'quantity':1}
    def test_cart_item_serializer(self):
        form = CartItemSerializer(data=self.data,context={'product':'2'})
        self.assertTrue(form.is_valid(), form.errors)
    def test_cart_item_serializer_with_envalid_quantity(self):
        form = CartItemSerializer(data=self.data)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertEqual(len(form.errors),1)
class OrderSerializerTest(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.address = baker.make(OrderAddress)
    def test_order_serializer(self):
        form = OrderSerializer(data={'user':self.user.id,'status':'sent','payment_status':'pending','total_price':234,
                                     'coupon':'sds','address':self.address.id}
                               )

        self.assertTrue(form.is_valid(), form.errors)









