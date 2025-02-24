from modeltranslation.translator import register, TranslationOptions
from .models import Product, Category,Brand,Variation,OrderAddress



@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    # required_languages = {'default': ('fa',)}
    # required_languages = ('en', 'fa') if you want to fill two field fa and en

@register(Category)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title',)
@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ('brand_name',)
@register(Variation)
class VariationTranslationOptions(TranslationOptions):
    fields = ('color', 'size','brands')
@register(OrderAddress)
class OrderAddressTranslationOptions(TranslationOptions):
    fields = ('addressCity','city','country')

