from rest_framework import serializers
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from .models import Product,ProductAttribute,ProductVariant

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


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['name', 'sku', 'mrp', 'weight', 'unit', 'description', 'product', 'attributes']

    attributes = serializers.ListField(child=serializers.IntegerField(), write_only=True)  # List of attribute IDs


    def create(self, validated_data):
        validated_data.pop('attributes')
        return ProductVariant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        product_variant = super().update(instance, validated_data)
        product_variant.save()

        return product_variant

class ProductVariantDetailSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    def get_product(self, instance):

        return instance.product.name
    def get_attributes(self,instance):
        att_list = []
        for att in instance.prdtattv_pdtv.all():
            att_list.append(att.attribute)
        return ProductAttributeSerializer(att_list,many=True).data

    class Meta:
        model = ProductVariant
        fields = ['id','name', 'sku', 'mrp', 'weight', 'unit', 'description', 'product', 'attributes']