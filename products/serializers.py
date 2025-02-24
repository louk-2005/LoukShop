#reset files
from rest_framework import serializers

#django files
from django.utils import timezone
from django.utils.translation import gettext_lazy as _




#your files
from .models.product_models import Category, Product, ProductVariant, Variation, Brand
from .models import Cart, CartItem, Coupon, Order, OrderItem, OrderAddress
from accounts.models import User



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'slug', 'parent', 'id']
        extra_kwargs = {
            'slug': {'read_only': True},
        }
class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand_name']
class VariantSerializer(serializers.ModelSerializer):
    brands = serializers.SerializerMethodField()
    class Meta:
        model = Variation
        fields = ['color','size','brands','id']
    def get_brands(self, obj):
        return BrandsSerializer(obj.brands.all(),many=True).data
class VariationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = ['color','size','brands']

    def create(self, validated_data):
        brands_data = validated_data.pop('brands', [])

        variation = Variation.objects.create(**validated_data)

        variation.brands.set(brands_data)
        return variation


class ProductVariantsSerializer(serializers.ModelSerializer):
    variation = serializers.SerializerMethodField()
    class Meta:
        model = ProductVariant
        fields = ['product','variation','additional_price']
    def get_variation(self, obj):
        return VariantSerializer(instance=obj.variation).data
class ProductSerializer(serializers.ModelSerializer):
    variants = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['title', 'slug', 'description', 'price', 'category','variants','is_active','created_at','updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']
    def get_variants(self, obj):
        return ProductVariantsSerializer(instance=obj.variations.all(), many=True).data
class ProductVariantsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        # extra_kwargs = {
        #     'additional_price':{'required':True},
        # }
    def create(self, validated_data):
        return ProductVariant.objects.create(**validated_data)

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError(_("User is required to create a cart."))
        return Cart.objects.create(user=user)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','phone']


class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    product_variant_info = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['cart','product','quantity','product_variant','user','product_variant_info']
        extra_kwargs = {
            'product': {'required': True},
            'quantity': {'required': True},
            'product_variant': {'required': True},
            'cart': {'required': False},
        }
    def get_product_variant_info(self, obj):
        return ProductVariantsSerializer(instance=obj.product_variant).data
    def validate_product_variantion(self, value):
        product = self.context.get('product')
        if not product:
            raise serializers.ValidationError(_('Product is not available'))
        print(value)
        if str(value.product.id) != product:
            raise serializers.ValidationError(_('Product_variation does not belong to this product'))
        return value

    def validate_quantity(self, value):
        product = self.context.get('product')
        if not product:
            raise serializers.ValidationError(_('Product is not available'))
        if value <= 0:
            raise serializers.ValidationError(_('Quantity must be a positive integer.'))
        product = Product.objects.filter(id=int(product)).first()
        if not product:
            raise serializers.ValidationError(_('Product is not available'))
        if not product.is_active:
            raise serializers.ValidationError(_('Product is not active'))
        return value


    def get_user(self, obj):
        return UserSerializer(instance=obj.cart.user).data

    def create(self, validated_data):
        user = self.context['request'].user
        if not user:
            raise serializers.ValidationError(_("User is required to create a cart item."))
        cart, created = Cart.objects.get_or_create(user=user)
        validated_data['cart'] = cart
        return CartItem.objects.create(**validated_data)
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code']
        extra_kwargs = {
            'code': {'required': True},
        }

    def validate_code(self, value):
        try:
            coupon = Coupon.objects.get(code=value)
            if not coupon.is_valid():
                raise serializers.ValidationError(_('Coupon code is not valid.'))
            return value
        except Coupon.DoesNotExist:
            raise serializers.ValidationError(_("Coupon does not exist."))

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = '__all__'
        extra_kwargs = {
            'address_in_city': {'required': True},
            'city': {'required': True},
            'country': {'required': True},
            'mobile_number': {'required': True},
        }
    def create(self, validated_data):
        return OrderAddress.objects.create(**validated_data)

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    address = OrderAddressSerializer(read_only=True)
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'order_date', 'status', 'total_price', 'coupon',
            'payment_status', 'items','address'
        ]
        read_only_fields = ['user', 'total_price', 'status', 'payment_status']
    def get_items(self, obj):
        return OrderItemSerializer(instance=obj.items.all(), many=True).data
class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'status': {'required': True},
            'payment_status': {'required': True},
            'total_price':{'required':False},
            'user':{'required':False},
            'address': {'required':True},
        }
    def create(self, validated_data):
        user = self.context['request'].user
        if not user:
            raise serializers.ValidationError(_("User is required to create a order."))
        cart = Cart.objects.get(user=user)
        if not cart:
            raise serializers.ValidationError(_("This user don't have any cart."))
        total_price = cart.get_total_price()
        if cart.discount_amount:
            total_price -= cart.discount_amount
        coupon=None
        if cart.coupon_code:
            coupon = Coupon.objects.get(code=cart.coupon_code)

        order = Order.objects.create(
            user=user,
            total_price=total_price,
            coupon=coupon,
            address=validated_data['address'],
            payment_status=validated_data['payment_status'],
            status=validated_data['status']
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product_variant=item.product_variant,
                quantity=item.quantity,
                product=item.product,
                final_price=item.product.price+item.product_variant.additional_price
            )

        return order
class ChangeStatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    class Meta:
        model = Order
        fields = ['status']
        extra_kwargs = {
            'status': {'required': True},
        }
    def validate_status(self, value):
        choices = [choice[0] for choice in Order.STATUS_CHOICES]
        if not value in choices:
            raise serializers.ValidationError(_('Status is not valid.'))
        return value
