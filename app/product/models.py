from django.db import models
from core.models import User
from category.models import Category

# Create your models here.
class Product(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=128, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.TextField(blank=True, null=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_created_user', blank=True,
                                null=True)
    updated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_updated_user', blank=True,
                                null=True)

    class Meta:
        db_table = 'Product'
class ProductAttribute(models.Model):

    Attribute_TYPE = (('Quantity', 'Quantity'), )
    type = models.CharField(choices=Attribute_TYPE, default="grocery", max_length=30)
    name = models.CharField(max_length=100,blank=True, null=True)
    unit = models.CharField(max_length=50,blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    attribute_label = models.CharField(max_length=200,blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productattribute_created_user', blank=True,
                                null=True)
    updated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productattribute_updated_user', blank=True,
                                null=True)



class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Product_variant')
    name =  models.CharField(max_length=300,blank=True, null=True)
    sku = models.CharField(max_length=50)
    mrp = models.FloatField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)
    #image_url = models.CharField(max_length=300,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productvariant_created_user', blank=True,
                                null=True)
    updated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productvariant_updated_user', blank=True,
                                null=True)




class ProductAttributeVariant(models.Model):
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='prdtattv_att')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='prdtattv_pdtv')
