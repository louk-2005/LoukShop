#django files
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient,APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from django.urls import reverse

#your files
from products.models import Product, Category,Cart,CartItem,Variation,ProductVariant
from products.serializers import ProductSerializer
from accounts.models import User

#other files
from model_bakery import baker

class ProductsViewTests(APITestCase):


    def setUp(self):
        self.user = User.objects.create_superuser(
            phone='testuser',
            email='alii@gmail.com',
            password='1'
        )

        self.client = APIClient()

        access = AccessToken.for_user(self.user)
        self.token = str(access)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.category = baker.make(Category,slug='sdfsfd')
        self.product = baker.make(Product,slug='sdf',category=self.category,description='sdf')


    def test_product_list_view_get(self):
        response = self.client.get(reverse('products:products-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['slug'], 'sdf')

    def test_product_list_view_post(self):


        response = self.client.post(reverse('products:products-list'),data={
        'title': 'Test Product',
        'category': self.category.id,
        'slug': 'Test-Product',
        'price': 234,
        'description': 'Test Product',
        'is_active': True
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)

    def test_product_detail_view_patch(self):
        response = self.client.patch(
            reverse('products:products-detail',
            args=[self.product.id]),
            data={'description': 'Test-uct'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], 'Test-uct')
    def test_product_detail_view_put(self):
        response = self.client.put(reverse('products:products-detail', args=[self.product.id]),
                                   data={
        'title': 'Test Product',
        'category': self.category.id,
        'slug': 'Test-Product',
        'price': 2343,
        'description': 'Test Product',
        'is_active': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['price'],'2343.00')
    def test_product_detail_view_delete(self):
        number_products = Product.objects.count()
        response = self.client.delete(
            reverse('products:products-detail',
            args=[self.product.id])
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), number_products-1)
class CategoryViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(phone='23423',email='alii@gmail.com',password='1')
        self.user1 = User.objects.create_user(phone='2342',email='aii@gmail.com',password='1')
        self.client = APIClient()
        access = AccessToken.for_user(self.user)
        self.token = str(access)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        # self.category1 = baker.make(Category,slug='sddf')
        self.category = baker.make(Category,slug='sdf')
    def test_category_list_view_get(self):
        response = self.client.get(reverse('products:categories-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['slug'], 'sdf')
        # print(response.data['results'][0]['slug'])
    def test_category_list_view_post(self):
        response = self.client.post(
            reverse('products:categories-list'),
            data={'slug':'23','title':'2323','parent':f'{self.category.id}'},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)
    def test_category_detail_view_patch(self):
        response = self.client.patch(reverse('products:categories-detail', args=[self.category.id]),
                                     data={'title':'34'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], '34')
    def test_category_detail_view_put(self):
        response = self.client.put(
            reverse('products:categories-detail',
            args=[self.category.id]),
            data={'slug':'34','title':'233'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        # print(response.data)
        self.assertEqual(response.data['title'],'233')


class CartViewTests(APITestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_superuser(phone='23423', email='alii@gmail.com', password='1')
        self.user1 = User.objects.create_user(phone='2342', email='aii@gmail.com', password='1')

        self.client = APIClient()
        self.factory = APIRequestFactory()
        access = AccessToken.for_user(self.user)
        self.token = str(access)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.cart = baker.make(Cart, user=self.user1)
        self.category = baker.make(Category, slug='sdf')
        self.product = baker.make(Product, category=self.category, slug='sdf', description='sdf')
        self.cart_item = baker.make(CartItem, cart=self.cart, product=self.product, quantity=1)

    def test_cart_list_view_get(self):
        response = self.client.get(reverse('products:cart-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 1)
