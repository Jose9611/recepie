from django.urls import path
from category import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateCategoryView.as_view(), name='create'),
    path('update/<int:pk>/', views.CategoryUpdateView.as_view(), name='update'),
    path('category-list/', views.CategoryListView.as_view(), name='category-list'),
]
