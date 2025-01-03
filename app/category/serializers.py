from rest_framework import serializers
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = Category
        fields = ['level', 'icon', 'name','created_at','main_category','icon_url','is_visible','priority','disclaimer']


    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        category = super().update(instance, validated_data)
        category.save()

        return category