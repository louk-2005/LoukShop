#django file
from django.db import models

#your file
from accounts.models import User
from products.models import ProductVariant, Product
from base import settings



class OrderAddress(models.Model):
    country = models.CharField(max_length=getattr(settings, 'COUNTRY_LENGHT',50),help_text='name of country')
    city = models.CharField(max_length=getattr(settings, 'CITY_LENGHT',50),help_text='name of city')
    addressCity = models.TextField(help_text='Your address in city')
    mobile_number = models.CharField(max_length=11)
    home_number = models.CharField(max_length=11)
    def __str__(self):
        return f'{self.country}___{self.mobile_number}___{self.addressCity}___{self.id}'

class Order(models.Model):
    STATUS_CHOICES = [
        ('canceled', 'Canceled'),
        ('delivered', 'Delivered'),
        ('sent', 'Sent'),
        ('registered', 'Registered'),
        ('processing', 'Processing'),
    ]
    PAYMENT_CHOICES = [
        ('pending', 'Pending'),
        ('canceled', 'Canceled'),
        ('processing', 'Processing'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='processing')
    address = models.ForeignKey(OrderAddress, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user.last_name} - {self.status}'

    class Meta:
        ordering = ['-order_date']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.order.user.last_name} - {self.product} - {self.quantity}'










