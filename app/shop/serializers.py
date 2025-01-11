from .models import Shop,Address,Inventory
from rest_framework import serializers

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['addr1', 'addr2', 'city', 'state', 'pincode']

class ShopSerializer(serializers.ModelSerializer):
    address_shop = AddressSerializer()
    """Serializer for the user object."""

    class Meta:
        model = Shop
        fields = ['id','name', 'admin', 'is_enabled','latitude','longitude','description','email','phone_number','website','created_at','updated_at','address_shop']

    def create(self, validated_data):
        address_data = validated_data.pop('address_shop', None)
        address = None
        if address_data:
            address = Address.objects.create(**address_data)

        shop = Shop.objects.create(address_shop=address, **validated_data)
        return shop

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address_shop',None)
        if address_data:
            address = instance.address_shop
            address.addr1 = address_data.get('addr1', address.addr1)
            address.addr2 = address_data.get('addr2', address.addr2)
            address.city = address_data.get('city', address.city)
            address.state = address_data.get('state', address.state)
            address.pincode = address_data.get('pincode', address.pincode)
            address.save()
        """Update and return user."""
        shop = super().update(instance, validated_data)
        shop.save()
        return shop


class InventorySerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = Inventory
        fields = ['id','shop','product_variant','price','quantity']


    def create(self, validated_data):
        return Inventory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        inventory = super().update(instance, validated_data)
        inventory.save()

        return inventory


class InventoryDetailSerializer(InventorySerializer):
    class Meta(InventorySerializer.Meta):
        fields = [field for field in InventorySerializer.Meta.fields if field not in ['shop', 'product_variant']]

    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)

        # Add custom fields
        representation['shop'] = instance.shop.name if instance.shop and instance.shop.name else None
        representation['variant'] = instance.product_variant.name if instance.product_variant and instance.product_variant.name else None
        representation['mrp'] = instance.product_variant.mrp if instance.product_variant and instance.product_variant.mrp else None
        return representation