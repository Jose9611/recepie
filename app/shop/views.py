from django.shortcuts import render
from rest_framework import generics,filters,status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from .serializers import ShopSerializer,InventorySerializer,InventoryDetailSerializer
from app.permission.custom_permission import IsAdmin,IsCustomer
from .models import Shop,Inventory
User = get_user_model()
from django.db.models import Case, When, F, Value, Subquery, OuterRef, BooleanField,Count,IntegerField,Sum
from rest_framework.response import Response
from .service.product_bulk_import import ProductCSVBulkCreateService
from .common.contants import MESSAGES
# Create your views here.
class CreateShopView(generics.CreateAPIView):
    serializer_class = ShopSerializer
    authentication_classes = [JWTAuthentication]  # Specify your authentication method
    permission_classes = [IsCustomer]

    def perform_create(self, serializer):
        shop = serializer.save(created_user=self.request.user)
        return shop

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = {}
        response.data['id'] = response.data.get('id')
        data['results'] = response.data
        data['message'] = "Shop sucessfully created"
        return Response(data, status=status.HTTP_201_CREATED)

class ShopUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsCustomer]

    def perform_update(self, serializer):
        # Ensure the `added_user` field stays the same during update
        shop = serializer.save(updated_user=self.request.user)  # Keep the added_user as the current user
        return shop

class ShopListView(generics.ListAPIView):
    queryset = Shop.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'name': ["in"],
        'phone_number': ["in"],
    }
    search_fields = ['name','phone_number']
    serializer_class = ShopSerializer
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsCustomer]  # Only authenticated users can view categories

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





class CreateInventoryView(generics.CreateAPIView):
    serializer_class = InventorySerializer
    authentication_classes = [JWTAuthentication]  # Specify your authentication method
    permission_classes = [IsCustomer]

    def perform_create(self, serializer):
        inventory = serializer.save(created_user=self.request.user)
        return inventory

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = {}
        response.data['id'] = response.data.get('id')
        data['results'] = response.data
        data['message'] = "inventory sucessfully created"
        return Response(data, status=status.HTTP_201_CREATED)


class InventoryUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsCustomer]

    def perform_update(self, serializer):
        # Ensure the `added_user` field stays the same during update
        inventory = serializer.save(updated_user=self.request.user)  # Keep the added_user as the current user
        return inventory

class InventoryListView(generics.ListAPIView):
    queryset = Inventory.objects.select_related('shop','product_variant','product_variant__product').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'product_variant__product__id': ["in"],
        'shop__id': ["in"],
    }
    search_fields = ['name','phone_number']
    serializer_class = InventoryDetailSerializer
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsCustomer]  # Only authenticated users can view categories

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

class ProductVariantCSVBulkCreate(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsCustomer]  # Only authenticated users can view categories


    def post(self, request):
        try:
            if request.FILES['file']:
                valid, data, is_empty = ProductCSVBulkCreateService.validate_csv(request.data)
                if not valid:

                    return Response({ 'results': [],'message':MESSAGES['INVALID_CSV']}, status=status.HTTP_409_CONFLICT)
                if is_empty:

                    return Response({ 'results': [],'message': MESSAGES['EMPTY_CSV']}, status=status.HTTP_409_CONFLICT)

                error = ProductCSVBulkCreateService.process_csv(data, request.user,action='create')
                if error:

                    return Response({'results': [], 'message': MESSAGES['ERROR_IN_CSV'],'error':error}, status=status.HTTP_409_CONFLICT)

                else:

                    return Response({'results': [],'message': MESSAGES['DONE'],'error': error}, status=status.HTTP_201_CREATED)
            else:

                return Response({'results': [],'message': MESSAGES['FAILED'],}, status=status.HTTP_409_CONFLICT)
        except Exception as ex:
            return Response({
                    'results': [],
                    'message': MESSAGES['FAILED'],

                }, status=status.HTTP_409_CONFLICT)