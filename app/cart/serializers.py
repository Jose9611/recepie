from .models import Cartitem,Cart
from rest_framework import serializers


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = Cartitem
        fields = ['id']

    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)

        # Add custom fields
        representation['product_name'] = instance.variant.name if instance.variant and instance.variant.name else None
        representation['mrp'] =  instance.variant.mrp if instance.variant and instance.variant.mrp else None
        representation['price'] = instance.inventory.price if instance.inventory and instance.inventory.price else None
        representation['quantity'] = instance.qty if instance.qty else None
        representation['total'] = instance.item_total
        representation['created_at'] = instance.created_at
        representation['updated_at'] = instance.updated_at
        return representation


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(source='cartitem_cart',many=True)

    """Serializer for the user object."""

    class Meta:
        model = Cart
        fields = ['id','user','shop', 'status', 'cart_items','created_at','updated_at']

    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)

        # Add custom fields
        representation['shop'] = instance.shop.name if instance.shop and instance.shop.name else None
        representation['user'] = instance.user.name if instance.user else None
        representation['grand_total'] = instance.grand_total if instance.grand_total else 0
        return representation


class CartAddCartItemSerializer(serializers.ModelSerializer):
    Id = serializers.SerializerMethodField()
    inventory_id = serializers.SerializerMethodField()
    shop_id = serializers.SerializerMethodField()
    cart_id = serializers.SerializerMethodField()

    def get_Id(self, obj):
        return obj.id

    def get_inventory_id(self, obj):
        return obj.inventory_id

    def get_shop_id(self, obj):
        return obj.cart.shop_id

    def get_cart_id(self, obj):
        return obj.cart_id

    class Meta:
        model = Cartitem
        exclude = ['id', 'inventory', 'cart']
        extra_fields = ['Id', 'shop_id', 'inventory_id', 'cart_id']