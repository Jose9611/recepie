from django.db import models
from core.models import User
from shop.models import Shop,Inventory
from product.models import ProductVariant
# Create your models here.
class Cart(models.Model):
    Status_TYPE = (('new', 'new'), ('transaction initiated', 'transaction initiated'), ('checked out', 'checked out'),
                   ('removed', 'removed'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_user')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='cart_shop')
    status = models.CharField(choices=Status_TYPE, default="new", max_length=30)
    region_id = models.IntegerField(blank=True, null=True)
    weight_id = models.IntegerField(blank=True, null=True)
    delivery_amt = models.FloatField(blank=True, null=True)
    est_distance = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Cart'
        app_label = 'cart'


class Cartitem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitem_cart')
    qty = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='cartitem_variant')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='cartitem_inventry')

    class Meta:
        db_table = 'CartItem'
        app_label = 'cart'