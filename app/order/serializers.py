
from .models import Order
from rest_framework import serializers


class OrderCreateSerializer(serializers.ModelSerializer):
    Id = serializers.SerializerMethodField()
    shop_id = serializers.SerializerMethodField()
    order_id = serializers.SerializerMethodField()
    additional_info = serializers.SerializerMethodField()

    def get_Id(self, obj):
        return obj.id

    def get_order_id(self, obj):
        return obj.order_id

    def get_shop_id(self, obj):
        return obj.shop.id

    def get_additional_info(self, obj):
        if not obj.additional_info:
            return ""
        return obj.additional_info


    class Meta:
        model = Order
        exclude = ('id', 'shop')
        extra_fields = ['Id', 'shop_id', 'order_id', 'final_price']