#django files
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin


#your files
from .models.product_models import Product,ProductVariant,Category,Brand,Variation
from .models.cart_models import Cart,CartItem,Coupon
from .models.order_models import OrderAddress, Order, OrderItem
from modeltranslation.admin import TranslationAdmin




@admin.register(Category)
class CategoryAdmin(TranslationAdmin,DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug')
    list_display_links = ('indented_title',)

@admin.register(Product)
class ProductAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'is_active', 'id')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('is_active', 'category')
    search_fields = ('title',)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'additional_price', 'variation','id')
    list_filter = ('product', 'variation')
    search_fields = ('product', 'variation')

class BrandAdmin(TranslationAdmin,admin.ModelAdmin):
    list_display = ('brand_name', 'id')
admin.site.register(Brand, BrandAdmin)

class VariationAdmin(TranslationAdmin,admin.ModelAdmin):
    list_display = ('color', 'size', 'get_brands')

    def get_brands(self, obj):
        return ' - '.join([brand.brand_name for brand in obj.brands.all()])

    get_brands.short_description = 'Brands'
    list_filter = ('color', 'size', 'brands')
    search_fields = ('color', 'size','brands__brand_name')
admin.site.register(Variation, VariationAdmin)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'created_at')
    def user_email(self, obj):
        return obj.user.email
    list_filter = ('user__email', 'created_at')
    search_fields = ('user__phone',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity','id')
    list_filter = ('cart', 'product')
    search_fields = ('cart', 'product')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent','created_at','updated_at')
    list_filter = ('code', 'discount_percent')
    search_fields = ('code',)

@admin.register(OrderAddress)
class OrderAddressAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ('addressCity', 'city')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'status','id')
    list_filter = ('user', 'status')
    search_fields = ('user', 'status')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'final_price')
    list_filter = ('order', 'product')
    search_fields = ('order', 'product')






