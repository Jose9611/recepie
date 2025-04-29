from django.urls import path
from . import views  # or import your views here

urlpatterns = [
    path('create/', views.CreateShopView.as_view(), name='create'),
    path('update/<int:pk>/', views.ShopUpdateView.as_view(), name='update'),
    path('shop-list/', views.ShopListView.as_view(), name='shop-list'),
    path('inventory-create/', views.CreateInventoryView.as_view(), name='shop-inventory'),
    path('inventory-update/<int:pk>/', views.InventoryUpdateView.as_view(), name='inventory-update'),
    path('inventory-list/', views.InventoryListView.as_view(), name='inventory-update'),
    path('product-import/', views.ProductVariantCSVBulkCreate.as_view(), name='product-import')

]