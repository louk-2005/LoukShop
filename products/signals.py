from django.db.models.signals import post_save, post_delete,pre_save
from django.core.cache import cache
from django.dispatch import receiver
from products.models import Product, Order, Coupon


@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    if created:
        cache.clear()

# Clear the cache for a specific order after it's created
@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if created:
        cache.clear()


@receiver(post_delete, sender=Product)
def product_post_delete(sender, instance, **kwargs):
    cache.clear()

@receiver(post_delete, sender=Order)
def order_post_delete(sender, instance, **kwargs):
    cache.clear()

#if you want delete the coupon after your apply order

# @receiver(post_save, sender=Order)
# def coupon_delete(sender, instance,created, **kwargs):
#     if created:
#         coupon = instance.coupon
#         print(coupon)
#         if coupon:
#             Coupon.objects.get(code=coupon).delete()

