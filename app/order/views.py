
from shop.common import CART_STATUS,USER
from shop.models import  Inventory, Shop
from cart.models import  Cartitem,Cart
from .models import Orderidcounter,Order,Orderupdates
from core.common import ShopBaseView
from rest_framework.views import APIView
from .serializers import OrderCreateSerializer
from app.permission.custom_permission import IsAdmin,IsCustomer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Case, When, F, Value, Subquery, OuterRef, BooleanField,Count,Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from shop.common import MESSAGES,ORDER_STATUS,ORDER_PAYMENT_TYPE
from rest_framework import generics,filters,status

class OrderCreateView(APIView,ShopBaseView):
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication
    permission_classes = [IsAdmin]
    """
        API to create a order.
    """

    def post(self, request):
        response = ''
        msg = ''
        data = {}
        tag = 'QS'

        try:
            total_price = 0
            total_weight = 0
            order_items = []

            if request.data:
                # data['user'] = request.user
                if not request.data.get("cart_items"):
                    return self.response(msg="Items are not selected", data=None, status=False)
                if not request.data.get("addr1"):
                    return self.response(msg="Address is not recognised", data=None, status=False)
                else:
                    data['addr1'] = request.data.get("addr1")
                if request.data.get("shop_id"):
                    data['shop_id'] = request.data.get("shop_id")

                cart = Cart.objects.filter(user=request.user, shop_id=request.data.get("shop_id"),
                                           status=CART_STATUS['NEW']).first()
                if not cart:
                    return self.response(msg="Failed to find the corresponding cart items", data=None, status=False)

                items = Cartitem.objects.all().select_related('cart', 'variant').select_related('variant__product') \
                    .filter(cart_id=cart.id, qty__gt=0)
                if not items:
                    return self.response(msg="Failed to find the corresponding cart items", data=None, status=False)
                shop = Shop.objects.get(id=request.data.get("shop_id"))


                data['status'] = ORDER_STATUS['Placed']
                if request.data.get('payment_type') and request.data.get('payment_type') == ORDER_PAYMENT_TYPE[
                    'COD']:
                    data['paymentkind'] = request.data.get('payment_type')
                if request.data.get('payment_type') and request.data.get('payment_type') == ORDER_PAYMENT_TYPE[
                    'OnlinePayment']:
                    data['status'] = ORDER_STATUS['PaymentPending']
                    data['paymentkind'] = request.data.get('payment_type')
                orderIdCount = Orderidcounter.objects.create(**{})
                order_id = tag + str(orderIdCount.id)
                if request.data.get('country'):
                    data['country'] = request.data.get('country')
                if request.data.get('state'):
                    data['state'] = request.data.get('state')

                if request.data.get('latitude'):
                    data['lat'] = request.data.get('latitude')
                if request.data.get('longitude'):
                    data['lon'] = request.data.get('longitude')

                if request.data.get('city'):
                    data['city'] = request.data.get('city')

                if request.data.get('pincode'):
                    data['pincode'] = request.data.get('pincode')

                if request.data.get('addr1'):
                    data['addr1'] = request.data.get('addr1')
                if request.data.get('addr2'):
                    data['addr2'] = request.data.get('addr2')
                if request.data.get('landmark'):
                    data['landmark'] = request.data.get('landmark')
                if request.data.get('phoneno'):
                    data['phoneno'] = request.data.get('phoneno')
                if request.data.get('additional_info'):
                    data['additional_info'] = request.data.get('additional_info')
                if request.data.get('to_name'):
                    data['to_name'] = request.data.get('to_name')
                else:
                    data['to_name'] = request.user.name
                if request.data.get('to_house_number'):
                    data['to_house_number'] = request.data.get('to_house_number')
                else:
                    data['to_house_number'] = "NA"
                if request.data.get('additional_info'):
                    data['additional_info'] = request.data.get('additional_info')
                else:
                    data['additional_info'] = ""

                if  request.data.get('total_price'):
                    total_price = request.data.get('total_price')

                data['total_price'] = total_price
                data['delivery_price'] = items[0].cart.delivery_amt
                data['estimated_distance'] = items[0].cart.est_distance
                data['order_id'] = order_id
                data['total_items'] = items.count()
                data['total_weight'] = total_weight
                data['cart'] = cart
                cart.status = CART_STATUS['TRANSACTION INITIATED']
                cart.save()

                order_obj = Order.objects.create(**data)
                inventory = Inventory.objects.filter(shop__id=shop.id)
                list_out = []
                for item in items:
                    item_dict = {}
                    item_dict['id'] = item.id
                    item_dict['product_id'] = item.variant.id
                    item_dict['product_name'] = item.variant.name if item.variant.name else item.variant.product.name
                    item_dict['product_mrp'] = item.variant.mrp
                    item_dict['product_price'] = inventory.get(product_variant_id=item.variant.id).price
                    item_dict['qty'] = item.qty
                    item_dict['sku'] = item.inventory.product_variant.sku
                    item_dict['weight'] = item.inventory.product_variant.weight
                    item_dict['shop_id'] = cart.shop.id
                    item_dict['unit'] = item.inventory.product_variant.unit

                    item_dict['order_id'] = order_obj.id
                    list_out.append(item_dict)

                order_obj.order_items = list_out
                order_obj.save()

                data = OrderCreateSerializer(order_obj)
                # if request.data.get('payment_type') == ORDER_PAYMENT_TYPE['COD']:
                order_updated = Orderupdates.objects.create(order_id=order_obj.order_id, status='Placed')
                # else:
                #     order_updated = Orderupdates.objects.create(order_id=order_obj.order_id, status='PaymentInitiated')


                data = data.data
                data['items'] = order_items

                cart.status = CART_STATUS['CHECKED_OUT']
                cart.save()
                response = self.response(
                    status=True,
                    msg=str(msg) if msg else "Done",
                    data={"order": data},
                )
        except Exception as ex:
            print(ex)
            response = self.response(
                status=False,
                data={},
                msg=MESSAGES["FAILED"]
            )
        return response
