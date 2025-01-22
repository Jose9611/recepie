import datetime
from django.db.models import  Q,F,Sum
from shop.common import CART_STATUS,USER
from shop.models import  Inventory, Shop
from cart.models import  Cartitem,Cart
from .models import Orderidcounter,Order
from core.common import ShopBaseView
from .serializers import CartAddCartItemSerializer,CartSerializer
from app.permission.custom_permission import IsAdmin,IsCustomer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Case, When, F, Value, Subquery, OuterRef, BooleanField,Count,Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from shop.common import MESSAGES,ORDER_STATUS,ORDER_PAYMENT_TYPE
from rest_framework import generics,filters,status

class OrderCreateView(ShopBaseView):
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
                data['user'] = request.user.user
                if not request.data.get("cart_items"):
                    return self.response(msg="Items are not selected", data=None, status=False)
                if not request.data.get("addr1"):
                    return self.response(msg="Address is not recognised", data=None, status=False)
                else:
                    data['addr1'] = request.data.get("addr1")

                cart = Cart.objects.filter(user=request.user, shop_id=request.data.get("shop_id"),
                                           status=CART_STATUS['NEW']).first()
                if not cart:
                    return self.response(msg="Failed to find the corresponding cart items", data=None, status=False)

                items = Cartitem.objects.all().select_related('cart', 'variant').select_related('variant__product') \
                    .filter(cart_id=cart.id, qty__gt=0)
                if not items:
                    return self.response(msg="Failed to find the corresponding cart items", data=None, status=False)






                data['total_price'] = total_price
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


                data['weight_id'] = items[0].cart.weight_id
                data['delivery_price'] = items[0].cart.delivery_amt
                data['estimated_distance'] = items[0].cart.est_distance
                data['order_id'] = order_id
                data['total_items'] = items.count()
                data['total_weight'] = total_weight
                discounted_price = round(data['discounted_price'], 2)
                delivery_amount = round(items[0].cart.delivery_amt, 2)
                total_price = round(total_price, 2)

                if discounted_price == total_price:
                    data['is_del_paid_by_customer'] = False
                elif delivery_amount + discounted_price == total_price:
                    data['is_del_paid_by_customer'] = True

                data['cart'] = cart
                cart.status = CART_STATUS['TRANSACTION INITIATED']
                cart.save()

                order_obj = Order.objects.create(**data)
                inventory = Inventory.objects.filter(shop__id=shop.id).prefetch_related('variant')
                list_out = []
                for item in items:
                    item_dict = {}
                    item_dict['id'] = item.id
                    item_dict['product_id'] = item.variant.id
                    item_dict['product_name'] = item.variant.name if item.variant.name else item.variant.product.name
                    item_dict['product_mrp'] = item.variant.mrp
                    item_dict['product_price'] = inventory.filter(product_variant_id=item.variant.id)
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

                campaign_id = request.data.get('campaign_id')
                if (request.data.get('payment_type') and request.data.get('payment_type') == ORDER_PAYMENT_TYPE[
                    'COD']) and order_updated and campaign_id:
                    UpdateCampaignData.update_campaign_data(order_obj, campaign_id, flag=1)
                data = data.data
                data['items'] = order_items

                cart.status = CART_STATUS['CHECKED_OUT']
                cart.save()

                if (request.data.get('payment_type') and request.data.get('payment_type') == ORDER_PAYMENT_TYPE[
                    'COD']):
                    notify_event_participants_order(order_obj.id, {
                        "status": order_obj.status,
                        "body": "Update on your order #{} from {}".format(order_obj.order_id, order_obj.shop.name),
                        "title": "Your order has been created",
                        "shop_id": order_obj.shop.id,
                        "imageUrl": "",
                        "order_id": str(order_obj.id),
                        "createdAt": DT.now().strftime(environ.DB_DATETIME_FORMAT)
                    })
                    if order_obj.shop.phone_number != None or order_obj.shop.phone_number != "":
                        send2FA(order_obj.user.phoneno, Template.Shop_OrderConfirm_Msg.value[0], order_obj.order_id)

                hash = OrderCreateService.shopHashWithDay(order_obj.shop.id)
                orderReport = Orderreportdaily.objects.filter(hash=hash, shop_id=order_obj.shop.id)
                if not orderReport:
                    Orderreportdaily.objects.create(hash=hash, shop_id=order_obj.shop.id, total_orders=1,
                                                    order_short_code='qwq')
                else:
                    Orderreportdaily.objects.filter(hash=hash, shop_id=order_obj.shop.id).update(
                        total_orders=F('total_orders') + 1)
                if payment_mode == ORDER_PAYMENT_TYPE['Wallet']:
                    erp_status = None
                    existing_wallet_transaction = ShopWalletTransaction.objects.filter(order=order_obj.id).first()
                    if not existing_wallet_transaction:  # payment mode is 'Wallet'
                        wallet_key = ShopWalletDeductMoney(order_obj)
                        print("OrderCreateView ErpShopCustomerWalletDeductAmount called", order_obj)
                        wallet = ShopWalletTransaction.objects.get(transaction_key=wallet_key)
                        try:
                            erp_status, response, err_msg = ErpShopCustomerWalletDeductAmount(
                                request_obj=wallet).process_erp_deduct_amount()
                        except Exception as e:
                            print("OrderCreateView ErpShopCustomerWalletDeductAmount process_erp_deduct_amount ex ", e)
                        wallet.is_erp_called = True
                        wallet.save()
                        if erp_status == ERP_REQUEST_STATUSES["pending"]:
                            order_obj.status = ORDER_STATUS['PAYMENTPENDING']
                            order_obj.save()

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


from django.shortcuts import render

# Create your views here.
