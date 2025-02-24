#django files
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

#your file
from accounts.models import User
from .product_models import ProductVariant, Product,Date
from django.utils import timezone
from base import settings


class Cart(Date):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carts') # OR user = models.OneToOneField(settings.AUTH_USER_MODELS, on_delete=models.CASCADE, related_name='carts')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon_code = models.CharField(max_length=getattr(settings, 'COUPON_CODE',10), default="")
    class Meta:
        ordering = ('created_at',)
    def get_total_price(self):
        total_price = 0

        for item in self.items.all():
            price = 0
            if item.product_variant.additional_price:
                price = item.quantity*(item.product.price+item.product_variant.additional_price)
            else:
                price = item.quantity*(item.product.price)
            total_price += price
        return total_price
    def __str__(self):
        return f'{self.user.email}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0,help_text="The quantity of item")
    class Meta:
        ordering = ('quantity',)

    def __str__(self):
        return f'{self.cart.user.email} | {self.product.title} | {self.quantity}'



class Coupon(Date):
    code = models.CharField(max_length=getattr(settings, 'COUPON_CODE',10),default="")
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_to
    def __str__(self):
        return self.code










