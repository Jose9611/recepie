from rest_framework import generics,filters,status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from .serializers import CategorySerializer
from app.permission.custom_permission import IsAdmin,IsCustomer
from .models import Category
User = get_user_model()
from django.db.models import Case, When, F, Value, Subquery, OuterRef, BooleanField,Count,IntegerField,Sum
from rest_framework.response import Response

class CreateCategoryView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]  # Specify your authentication method
    permission_classes = [IsCustomer]

    def perform_create(self, serializer):
        category = serializer.save(added_user=self.request.user)
        return category

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = {}
        response.data['id'] = response.data.get('id')
        data['results'] = response.data
        data['message'] = "Category sucessfully created"
        return Response(data, status=status.HTTP_201_CREATED)


class CategoryUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsCustomer]

    def perform_update(self, serializer):
        # Ensure the `added_user` field stays the same during update
        category = serializer.save(updated_user=self.request.user)  # Keep the added_user as the current user
        return category


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'level': ["exact"],
        'name': ["in"],
        'main_category__id': ["in"],
    }
    search_fields = ['name']
    serializer_class = CategorySerializer
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



