from django.db import models
from core.models import User
from shop.models import Shop
from cart.models import Cart
from django.contrib.postgres.fields import ArrayField
from safedelete.models import SafeDeleteModel, SOFT_DELETE


# Create your models here.
class Orderidcounter(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = 'OrderIdCounter'


class CancellationChoices(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    type = models.CharField(max_length=500, blank=False, null=False)
    sort = models.IntegerField(null=True, blank=True, default=0)
    user_type = models.IntegerField(null=False)

    class Meta:
        db_table = 'CancellationChoices'

class Order(models.Model):
    ORDER_STATUS = (
        ('PaymentDone', 'PaymentDone'),
        ('PaymentPending', 'PaymentPending'),
        ('PaymentFailed', 'PaymentFailed'),
        ('Placed', 'Placed'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Modified', 'Modified'),
        ('Delivered', 'Delivered'),
        ('CancelledCustomer', 'CancelledCustomer'),
        ('CancelledMerchant', 'CancelledMerchant'),
        ('Undelivered', 'Undelivered'))

    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_created_user',  blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    discounted_price = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    total_items = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    expected_time_minutes = models.IntegerField(default=0)
    addr1 = models.TextField(null=True, blank=True)
    addr2 = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(null=True, blank=True)
    landmark = models.TextField(null=True, blank=True)
    lat = models.FloatField()
    lon = models.FloatField()
    phoneno = models.TextField(null=True, blank=True)
    pincode = models.TextField(blank=True, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='order_shop')
    state = models.TextField(blank=True, null=True)
    status = models.TextField(choices=ORDER_STATUS)
    order_id = models.TextField(unique=True)
    discount_code = models.TextField(blank=True, null=True)
    total_weight = models.FloatField()
    delivery_price = models.FloatField(blank=True, null=True)
    prod_discount = models.FloatField(blank=True, null=True, default=0)
    del_discount = models.FloatField(blank=True, null=True, default=0)
    has_been_refunded = models.BooleanField(default=False)
    estimated_distance = models.FloatField(blank=True, null=True)
    delivery_order_id = models.TextField(blank=True, null=True)
    modification_count = models.IntegerField(default=0)
    to_name = models.TextField(null=True, blank=True)
    locality = models.TextField(null=True, blank=True)
    to_house_number = models.TextField(null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order_cartitems')
    order_items = ArrayField(models.JSONField(), blank=True, null=True, default=list)
    cancellation_choices = models.ForeignKey(CancellationChoices, null=True, on_delete=models.SET_NULL)
    cancellation_comment = models.TextField(blank=True, null=True, max_length=500)
    cancelled = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_cancelled_user', blank=True,
                                  null=True)

class Orderupdates(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    order = models.ForeignKey(Order, to_field="order_id", db_column="order_id", on_delete=models.CASCADE,
                              related_name='orderupdates')
    status = models.TextField()  # This field type is a guess.
    created_at = models.DateTimeField(auto_now_add=True)
    modification = models.TextField(blank=True, null=True)
    modified_by = models.TextField(blank=True, null=True)
