import datetime
from django.db.models import  Q,F
from shop.common import CART_STATUS,USER
from shop.models import  Inventory, Shop
from .models import Cartitem,Cart
from rest_framework.views import APIView
from .serializers import CartAddCartItemSerializer,CartSerializer
from app.permission.custom_permission import IsAdmin,IsCustomer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Case, When, F, Value, Subquery, OuterRef, BooleanField,Count,IntegerField,Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from shop.common import MESSAGES
from rest_framework import generics,filters,status

class add_cart_item(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsCustomer]

    def post(self, request):
        cart_id = request.data.get('cart_id')
        qty = request.data.get('qty')
        shop_id = request.data.get('shop_id')
        inventory_id = request.data.get('inventory_id')
        user = request.user


        try:
            cart_exist = Cart.objects.filter(Q(user=user) & Q(shop_id=shop_id) & Q(status=CART_STATUS['NEW'])).first()
            inventory = Inventory.objects.filter(shop_id=shop_id, id=inventory_id).first()
            if not inventory:
                return self.response(data=[], msg="Item does not exits", status=False)
            if not Shop.objects.filter(id=shop_id).exists():
                return self.response(data=[], msg="Shop does not exists", status=False)

            if cart_exist is None:
                cart_create = Cart.objects.create(shop_id=shop_id, status=CART_STATUS['NEW'],
                                                  user=user)
                item = Cartitem.objects.create(qty=int(qty), cart=cart_create, inventory=inventory,variant=inventory.product_variant)
                item = CartAddCartItemSerializer(item, read_only=True).data
                return self.response(data={'item': item}, msg="done", status=True)

            else:
                cart_items = Cartitem.objects.filter(cart_id=cart_exist.id, inventory_id=inventory_id)

                if cart_items.count() == 0:
                    item = Cartitem.objects.create(qty=int(qty), cart=cart_exist, inventory=inventory,variant=inventory.product_variant)

                    item = CartAddCartItemSerializer(item, read_only=True).data
                    cart_exist.updated_on = datetime.datetime.now()
                    cart_exist.save()
                    return Response({"message":MESSAGES["Done"]}, status=status.HTTP_201_CREATED)

                else:

                    cart_items.update(qty=F('qty') + 1)
                    already_added = CartAddCartItemSerializer(cart_items.first(), read_only=True).data
                    cart_exist.updated_on = datetime.datetime.now()
                    cart_exist.save()
                    return Response({'item': "already_added","message":"Item already exists. Updating quantity."}, status=status.HTTP_201_CREATED)

            item_data = Inventory.objects.filter(shop_id=shop_id, id=inventory_id)
            if item_data is None:
                return self.response({"message":"Item does not exits"}, status=status.HTTP_409_CONFLICT)
            shop_exist = Shop.objects.filter(id=shop_id)

            if shop_exist.count() == 0:
                return Response({"message":"Shop does not exists"}, status=status.HTTP_409_CONFLICT)
        except Exception as ex:
            response = Response({ "message":"something wrong"}, status=status.HTTP_409_CONFLICT)

        return response

class CartListView(generics.ListAPIView):
    queryset = Cart.objects.select_related('shop','user').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'user__id': ["in"],
        'shop__id': ["in"],
    }
    search_fields = ['name','phone_number']
    serializer_class = CartSerializer
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
