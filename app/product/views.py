from rest_framework import generics, filters,status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from .serializers import ProductSerializer,ProductAttributeSerializer,ProductVariantSerializer,ProductVariantDetailSerializer
from app.permission.custom_permission import IsAdmin, IsCustomer
from .models import Product,ProductAttribute,ProductAttributeVariant,ProductVariant
from django.db.models import Case, When, F, Value, Subquery, OuterRef, BooleanField,Count,IntegerField,Sum
from rest_framework.response import Response
User = get_user_model()


class CreateProductView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]  # Specify your authentication method
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        product = serializer.save(created_user=self.request.user)
        return product

    def create(self, request, *args, **kwargs):

        response = super().create(request, *args, **kwargs)
        data = {}
        response.data['id'] = response.data.get('id')
        data['results'] = response.data
        data['message'] = "Product sucessfully created"
        return Response(data,status=status.HTTP_201_CREATED)

class ProductUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsAdmin]

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
    permission_classes = [IsAdmin]  # Only authenticated users can view categories

    def list(self, request, *args, **kwargs):
        try:
            # filtered_queryset = self.get_queryset()
            queryset = self.filter_queryset(self.queryset)
            count = queryset.aggregate(total_count=Count('id'))

            # Pagination parameters
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                paginated_response = self.get_paginated_response(serializer.data)
                paginated_response.data['total_count'] = count
                return paginated_response

            # If pagination is not applied, return all results
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'results': serializer.data,
                'total_count': count,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': '0', 'error': str(e)}, status=status.HTTP_409_CONFLICT)





class CreateProductAttributeView(generics.CreateAPIView):
    serializer_class = ProductAttributeSerializer
    authentication_classes = [JWTAuthentication]  # Specify your authentication method
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        product_attribute = serializer.save(created_user=self.request.user)
        return product_attribute

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = {}
        response.data['id'] = response.data.get('id')
        data['results'] = response.data
        data['message'] = "Product Attribute sucessfully created"
        return Response(data, status=status.HTTP_201_CREATED)


class ProductAttributeUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsAdmin]

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
    permission_classes = [IsAdmin]  # Only authenticated users can view categories

    def list(self, request, *args, **kwargs):
        try:
            # filtered_queryset = self.get_queryset()
            queryset = self.filter_queryset(self.queryset)
            count = queryset.aggregate(total_count=Count('id'))

            # Pagination parameters
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                paginated_response = self.get_paginated_response(serializer.data)
                paginated_response.data['total_count'] = count
                return paginated_response

            # If pagination is not applied, return all results
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'results': serializer.data,
                'total_count': count,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': '0', 'error': str(e)}, status=status.HTTP_409_CONFLICT)



class CreateProductVariantView(generics.CreateAPIView):
    serializer_class = ProductVariantSerializer  # Your ProductVariant serializer
    authentication_classes =  [JWTAuthentication]    # Specify your authentication method
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        # Extract data from the request for the Product and ProductAttribute
        product = Product.objects.get(id=self.request.data.get('product'))  # Get the Product by ID
        attributes_ids = self.request.data.get('attributes', [])  # Get a list of ProductAttribute IDs

        # Create and save the ProductVariant object
        product_variant = serializer.save(
            created_user=self.request.user,  # Set the user who is creating the product variant
            product=product,  # Link the Product
        )

        # If there are attributes provided, associate them with the ProductVariant
        for attribute_id in attributes_ids:
            try:
                attribute = ProductAttribute.objects.get(id=attribute_id)
                ProductAttributeVariant.objects.create(attribute=attribute, variant=product_variant)
            except ProductAttribute.DoesNotExist:
                # Handle the case where the ProductAttribute doesn't exist
                pass

        return product_variant  # Return the created ProductVariant

    def create(self, request, *args, **kwargs):

        response = super().create(request, *args, **kwargs)
        data = {}
        response.data['id'] = response.data.get('id')
        data['results'] = response.data
        data['message'] = "Product Variant sucessfully created"
        return Response(data, status=status.HTTP_201_CREATED)


class ProductvariantUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class =  ProductVariantSerializer
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsAdmin]

    def perform_update(self, serializer):
        # Ensure the `added_user` field stays the same during update
        attributes_ids = self.request.data.get('attributes', [])
        product_variant = serializer.save(updated_user=self.request.user)  # Keep the added_user as the current user
        ProductAttributeVariant.objects.filter(variant=product_variant).delete()
        for attribute_id in attributes_ids:
            try:
                attribute = ProductAttribute.objects.get(id=attribute_id)
                ProductAttributeVariant.objects.create(attribute=attribute, variant=product_variant)
            except ProductAttribute.DoesNotExist:
                # Handle the case where the ProductAttribute doesn't exist
                pass

        return product_variant

class ProductvariantListView(generics.ListAPIView):
    queryset = ProductVariant.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'name': ["in"],
    }
    search_fields = ['name']
    serializer_class = ProductVariantDetailSerializer
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsAdmin]  # Only authenticated users can view categories

    def list(self, request, *args, **kwargs):
        try:
            # filtered_queryset = self.get_queryset()
            queryset = self.filter_queryset(self.queryset)
            count = queryset.aggregate(total_count=Count('id'))

            # Pagination parameters
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                paginated_response = self.get_paginated_response(serializer.data)
                paginated_response.data['total_count'] = count
                return paginated_response

            # If pagination is not applied, return all results
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'results': serializer.data,
                'total_count': count,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': '0', 'error': str(e)}, status=status.HTTP_409_CONFLICT)







