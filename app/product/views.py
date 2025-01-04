from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from .serializers import ProductSerializer,ProductAttributeSerializer
from app.permission.custom_permission import IsAdmin, IsCustomer
from .models import Product,ProductAttribute

User = get_user_model()


class CreateProductView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]  # Specify your authentication method
    permission_classes = [IsCustomer]

    def perform_create(self, serializer):
        product = serializer.save(created_user=self.request.user)
        return product


class ProductUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsCustomer]

    def perform_update(self, serializer):
        # Ensure the `added_user` field stays the same during update
        product = serializer.save(updated_user=self.request.user)  # Keep the added_user as the current user
        return product

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'name': ["in"],
        'category__id': ["in"],
    }
    search_fields = ['name']
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsCustomer]  # Only authenticated users can view categories





class CreateProductAttributeView(generics.CreateAPIView):
    serializer_class = ProductAttributeSerializer
    authentication_classes = [JWTAuthentication]  # Specify your authentication method
    permission_classes = [IsCustomer]

    def perform_create(self, serializer):
        product_attribute = serializer.save(created_user=self.request.user)
        return product_attribute


class ProductAttributeUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsCustomer]

    def perform_update(self, serializer):
        # Ensure the `added_user` field stays the same during update
        product_attribute = serializer.save(updated_user=self.request.user)  # Keep the added_user as the current user
        return product_attribute

class ProductAttributeListView(generics.ListAPIView):
    queryset = ProductAttribute.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'name': ["in"],
        'unit': ["in"],
    }
    search_fields = ['name']
    serializer_class = ProductAttributeSerializer
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsCustomer]  # Only authenticated users can view categories





