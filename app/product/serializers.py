from rest_framework import serializers
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from .models import Product,ProductAttribute

class ProductAttributeSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = ProductAttribute
        fields = ['id','type','name','unit','value','attribute_label']


    def create(self, validated_data):
        return ProductAttribute.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        product_attribute = super().update(instance, validated_data)
        product_attribute.save()

        return product_attribute

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = Product
        fields = ['id','name','category','description','manufacturer','created_at']


    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        product = super().update(instance, validated_data)
        product.save()

        return product