#rest files
from rest_framework import viewsets, permissions,status
from rest_framework.decorators import  action as Action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework_tracking.mixins import LoggingMixin


#django files
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.decorators import method_decorator

#your files
from .models import Order
from .models.product_models import Category, Product, Brand,Variation, ProductVariant
from .serializers import (CategorySerializer, ProductSerializer, BrandsSerializer,
                          ProductVariantsSerializer, VariationCreateSerializer, ProductVariantsCreateSerializer,
                          VariantSerializer, CartItemSerializer, CouponSerializer, OrderSerializer,
                          OrderCreateSerializer,ChangeStatusSerializer,CartSerializer)
from utils.filters import ProductFilter
from .models.cart_models import CartItem,Coupon,Cart
from utils.custom_pagination import CustomPagination




class CategoryViewSet(viewsets.ModelViewSet):
    """
    this is viewset View for Category model
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get_permissions(self):
        if self.action in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

class ProductViewSet(LoggingMixin,viewsets.ModelViewSet):#because you using logginMixin you can't see the error in postman but you can see them in admin panel
    """
    this is viewset View for Product model
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ['title','=price']

    def get_permissions(self):
        if self.action in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    # @method_decorator(cache_page(60 * 15))  when using this your filter and pagination don't work because after first time it using cache memory
    #to read the information and filter is don't work to because def list serializer.data
    # def list(self, request, *args, **kwargs):
    #     queryset = self.queryset.all()
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)


    @Action(detail=True, methods=['GET'])
    def products_with_similar_category(self, request, pk=None):
        """
        this is viewset View for Product model that allow you to saw similar products
        """
        cache_key = f'{Product.objects.get(pk=pk).pk}:products_with_similar_category'
        cache_value = cache.get(cache_key)
        if not cache_value:
            product = self.get_object()
            similar_products = Product.objects.filter(category=product.category)
            serializer = ProductSerializer(similar_products, many=True)
            cache.set(cache_key, serializer.data, timeout=60*15)
            cache_value = serializer.data
        return Response(cache_value)
class BrandViewSet(viewsets.ModelViewSet):
    """
    this is viewset View for Brand model
    """
    queryset = Brand.objects.all()
    serializer_class = BrandsSerializer

    def get_permissions(self):
        if self.action in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
class VariationViewSet(viewsets.ModelViewSet):
    """
    this is viewset View for Variation model
    """
    queryset = Variation.objects.all()
    serializer_class = VariationCreateSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve','get']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
    def get_serializer_class(self):
        if self.action in permissions.SAFE_METHODS:
            return VariantSerializer
        return VariationCreateSerializer
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        queryset=self.queryset
        serializer = VariantSerializer(queryset, many=True)
        return Response(serializer.data)
class ProductsVariationViewSet(viewsets.ModelViewSet):
    """
    this is viewset View for Product model
    """
    queryset = ProductVariant.objects.all()
    def get_serializer_class(self, *args, **kwargs):
        if self.action in ['list', 'retrieve','get']:
            return ProductVariantsSerializer
        return ProductVariantsCreateSerializer
    def get_permissions(self):
        if self.action in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class CartViewSet(viewsets.ModelViewSet):
    """
    this is viewset View for Cart
    """
    serializer_class = CartItemSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()]
    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return CartItem.objects.all()
        else:
            return CartItem.objects.filter(cart__user=self.request.user)
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['product'] = self.request.data.get('product')
        return context
    @Action(detail=False, methods=['POST'])
    def apply_coupon(self, request):
        serializer = CouponSerializer(data=request.data)

        if serializer.is_valid():
            try:
                cd = serializer.validated_data
                coupon = Coupon.objects.get(code=cd.get('code'))
                cart = Cart.objects.get(user=request.user)
                discount_amount = (cart.get_total_price() * coupon.discount_percent) / 100
                cart.discount_amount = discount_amount
                cart.coupon_code = cd.get('code')
                cart.save()
                return Response({'message': _('Discount applied successfully'), 'data': serializer.data},
                                status=status.HTTP_200_OK)
            except Cart.DoesNotExist:
                return Response({'message': _('Cart not found for this user')}, status=status.HTTP_404_NOT_FOUND)
            except Coupon.DoesNotExist:
                return Response({'message': _('Coupon does not exist')}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': _('Invalid coupon'), 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    """
    this is viewset View for Order
    """
    queryset = Order.objects.all()
    throttle_scope = 'order'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_permissions(self):
        if self.action in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve','get']:
            return OrderSerializer
        return OrderCreateSerializer

    def list(self, request, *args, **kwargs):
        cache_key = f"user_orders_{request.user.id}"
        cached_orders = cache.get(cache_key)

        if not cached_orders:
            orders = self.queryset.filter(user=request.user)
            serializer = self.get_serializer_class()(instance=orders, many=True)
            cache.set(cache_key, serializer.data, timeout=60 * 30)
            cached_orders = serializer.data

        return Response(cached_orders, status=status.HTTP_200_OK)
    @Action(detail=True, methods=['PATCH'])
    def status(self, request, pk=None):
        """
        this is viewset View for Order model that allow you to change status
        """
        order = self.get_object()
        serializer = ChangeStatusSerializer(data=request.data)
        if serializer.is_valid():
            order.status = serializer.validated_data.get('status')
            order.save()
            return Response(
            {'message':(_('Status change successfully')),'data':serializer.data},
                 status=status.HTTP_200_OK
            )
        return Response(
            {'message':(_('invalid argument')),'data':serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )














