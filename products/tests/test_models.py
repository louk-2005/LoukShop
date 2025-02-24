#django files
from django.test import TestCase
from django.db import IntegrityError

#other files
from model_bakery import baker

#your files
from products.models import (Product, Category, Cart, CartItem, OrderItem, Order, Variation, ProductVariant,
                             Brand,OrderAddress)
from accounts.models import User



class CategoryModelTest(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(title='test', slug='sdf')
    def test_category_unique_title(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(title='test', slug='sdf')
    def test_category_unique_slug(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(title='test', slug='sdf')
    def test_category_str(self):
        self.assertEqual(str(self.category1), 'test')
class ProductModelTest(TestCase):
    def setUp(self):
        self.category = baker.make(Category,slug='test')
    def test_product_str(self):
        product = baker.make(Product,slug='test',title='test',description='test',category=self.category)
        self.assertEqual(str(product), 'test - test')

class VariationModelTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(brand_name='test')
        self.brand1 = Brand.objects.create(brand_name='test1')

    def test_variation_str(self):
        variation = Variation.objects.create(color='red',size='small')
        variation.brands.set([self.brand,self.brand1])
        self.assertEqual(str(variation), 'red - small - (test-test1)')
        # print(str(variation))
class ProductVariantModelTest(TestCase):
    def setUp(self):
        self.variation = Variation.objects.create(color='red',size='small')
        self.category = baker.make(Category,slug='test')
        self.product = baker.make(Product,slug='test',title='test',description='test',category=self.category)
    def test_product_variant_str(self):
        variation = ProductVariant.objects.create(product=self.product,variation=self.variation,additional_price=345)
        self.assertEqual(str(variation), '345')

class CartModelTest(TestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.user1 = baker.make(User,email='ali=@gmail.com')

        self.category = baker.make(Category, slug='test', parent=None)
        self.product = baker.make(Product, slug='sdf', description='Test Product', category=self.category,
                                 is_active=True, id=2)
        self.variation = baker.make(Variation)
        self.cart = baker.make(Cart,user=self.user)

        self.productVariant = baker.make(ProductVariant, variation=self.variation, product=self.product)
        self.data = {'product_variant': self.productVariant.id, 'product': self.product.id, 'cart': self.cart.id,
                     'quantity': 1}

    def test_cart_str(self):
        cart = baker.make(Cart,user=self.user1)
        self.assertEqual(str(cart), 'ali=@gmail.com')

    def test_cart_total_price(self):
        cart = baker.make(Cart, user=self.user1)

        cartItem = CartItem.objects.create(cart=cart, product_variant=self.productVariant, quantity=1,product=self.product)
        price = (cartItem.product.price+self.productVariant.additional_price)*cartItem.quantity
        self.assertEqual(cart.get_total_price(), price)
        # print(price)
        # print(cart.get_total_price())
class OrderModelTest(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.address = baker.make(OrderAddress)

    def test_order_str(self):
        order = baker.make(Order,user=self.user,status='sent',payment_status='pending',address=self.address)
        self.assertEqual(str(order), f'{self.user.last_name} - sent')
    def test_order_Invalid_status(self):
        # with self.assertRaises(IntegrityError):
        order = baker.make(Order,user=self.user,status='sen',payment_status='pending',address=self.address)
        status=['sent','processing','canceled','delivered','registered']
        self.assertNotIn(order.status,status)
        # print(order.status)
class CartItemModelTest(TestCase):
    def setUp(self):
        self.category = baker.make(Category, slug='test', parent=None)
        self.product = baker.make(Product, slug='sdf', description='Test Product', category=self.category,
                                  is_active=True, id=2)
        self.cart = baker.make(Cart)
        self.variation = baker.make(Variation)
        self.productVariant = baker.make(ProductVariant, variation=self.variation, product=self.product)
        self.data = {'product_variant': self.productVariant.id, 'product': self.product.id, 'cart': self.cart.id,
                     'quantity': 1}
    def test_cart_item_str(self):
        cartItem = CartItem.objects.create(cart=self.cart, product_variant=self.productVariant, quantity=1,product=self.product)
        self.assertEqual(str(cartItem), f'{self.cart.user.email} | {self.product.title} | 1')







