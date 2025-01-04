from rest_framework import generics,filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from .serializers import CategorySerializer
from app.permission.custom_permission import IsAdmin,IsCustomer
from .models import Category
User = get_user_model()



class CreateCategoryView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]  # Specify your authentication method
    permission_classes = [IsCustomer]

    def perform_create(self, serializer):
        category = serializer.save(added_user=self.request.user)
        return category

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


