from django.urls import path
from . import views  # or import your views here

urlpatterns = [
    path('add-item/', views.add_cart_item.as_view(), name='add-item'),
    path('cart-list/', views.CartListView.as_view(), name='cart-list'),
    path('user-cart-list/', views.UserCartListView.as_view(), name='user-cart-list')
]
