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
        fields = ['id','level', 'icon', 'name','main_category','icon_url','is_visible','priority','disclaimer','created_at','updated_at']


    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        category = super().update(instance, validated_data)
        category.save()

        return category