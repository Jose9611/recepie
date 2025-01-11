from django.db import models
from core.models import User
from product.models import ProductVariant
# Create your models here.

class Address(models.Model):
    addr1 = models.CharField(max_length=128,blank=True,null=True)
    addr2 = models.CharField(max_length=128,blank=True,null=True)
    city = models.CharField(max_length=128,blank=True,null=True)
    pincode = models.CharField(max_length=12,blank=True,null=True)
    state = models.CharField(max_length=128,blank=True,null=True)

    class Meta:
        db_table = 'Address'


class Shop(models.Model):
    name = models.CharField(max_length=256)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_admin')
    is_enabled = models.BooleanField(default=False)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    description = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    send_sms_confirmation = models.BooleanField(default=False)
    website = models.TextField(blank=True, null=True)
    service_distance_meters = models.IntegerField(default=3000)
    address_shop = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='shop', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_created_user', blank=True,
                                null=True)
    updated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_updated_user', blank=True,
                                null=True)
    delivery_service = models.BooleanField(default=False)

    class Meta:
        db_table = 'Shop'




class Inventory(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='inventory_shop')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='inventory_variant')
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0)
    is_enabled = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_scheduled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory_created_user', blank=True,null=True)
    updated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory_updated_user', blank=True,
                                null=True)

    class Meta:
        db_table = 'Inventory'



class Availableday(models.Model):
    schedule_start = models.TimeField(blank=True, null=True)
    schedule_end = models.TimeField(blank=True, null=True)
    day = models.IntegerField(default=0)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='available_inventory')

    class Meta:
        db_table = 'AvailableDay'
