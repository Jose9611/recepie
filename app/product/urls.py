from django.urls import path
from product import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateProductView.as_view(), name='create'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='update'),
    path('product-list/', views.ProductListView.as_view(), name='product-list'),

    path('attribute-create/', views.CreateProductAttributeView.as_view(), name='attribute-create'),
    path('attribute-update/<int:pk>/', views.ProductAttributeUpdateView.as_view(), name='attribute-update'),
    path('attribute-list/', views.ProductAttributeListView.as_view(), name='attribute-list'),
]
