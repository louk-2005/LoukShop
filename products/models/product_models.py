#django files
from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField


#your files
from base import settings


class Date(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True



class Category(MPTTModel):
    title = models.CharField(max_length=100, unique=True,help_text='write your title')
    slug = AutoSlugField(populate_from='title', unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    def __str__(self):
        return self.title


    class MPTTMeta:
        order_insertion_by = ['title']


    def __str__(self):
        return self.title

class Product(Date):
    title = models.CharField(max_length=getattr(settings,'TITLE_LENGTH',100),help_text='write your title')
    slug = AutoSlugField(populate_from='title',  unique_with=('created_at','id'))
    description = RichTextUploadingField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f'{self.title} - {self.description[0:50]}'

    class Meta:
        ordering = ['title']

class Brand(models.Model):
    brand_name = models.CharField(max_length=getattr(settings,'BRAND_LENGTH',100),help_text='write your brand name')

    def __str__(self):
        return self.brand_name

    class Meta:
        ordering = ['brand_name']

class Variation(models.Model):
    color = models.CharField(max_length=100, help_text='color of product')
    size = models.CharField(max_length=100, help_text='size of product')
    brands = models.ManyToManyField(Brand, related_name='variations')
    def __str__(self):
        brands_name='-'.join([brand.brand_name for brand in self.brands.all()])
        return f'{self.color} - {self.size} - ({brands_name})'


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    variation = models.ForeignKey(Variation, related_name='Vproducts', on_delete=models.CASCADE)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f'{self.additional_price}'
