import datetime
from django.db.models import  Q,F
from shop.common.common.constants import CART_STATUS,USER
from shop.models import Cartitem, Cart, Inventory, Shop
from shop.admin.serializers.cart import CartAddCartItemSerializer
from rest_framework.views import APIView

class add_cart_item(APIView):
    def post(self, request):
        cart_id = request.data.get('cart_id')
        qty = request.data.get('qty')
        shop_id = request.data.get('shop_id')
        inventory_id = request.data.get('inventory_id')
        user = request.user
        if user is not None:
            if user.user.role.id != USER['USER']:
                return self.response(data=[], msg="User not permitted", status=False)
        else:
            return self.response(data=[], msg="Unauthorized user", status=False)


        try:
            cart_exist = Cart.objects.filter(Q(user_cart=user.user.user_cart)&Q(shop_id=shop_id)&Q(status=CART_STATUS['NEW'])).first()
            inventory = Inventory.objects.filter(shop_id=shop_id, id=inventory_id)
            if not inventory.exists():
                return self.response(data=[], msg="Item does not exits", status=False)
            if not Shop.objects.filter(id=shop_id).exists():
                return self.response(data=[], msg="Shop does not exists", status=False)

            if cart_exist is None:
                cart_create = Cart.objects.create( shop_id=shop_id, status=CART_STATUS['NEW'],
                                                  user_cart=user.user.user_cart)
                item = Cartitem.objects.create(qty=int(qty), cart=cart_create, inventory=inventory.first())
                item = CartAddCartItemSerializer(item, read_only=True).data
                return self.response(data={'item': item}, msg="done", status=True)

            else:
                cart_items = Cartitem.objects.filter(cart_id=cart_exist.id, inventory_id=inventory_id)

                if cart_items.count() == 0:
                    item = Cartitem.objects.create(qty=int(qty), cart=cart_exist, inventory=inventory.first())

                    item = CartAddCartItemSerializer(item, read_only=True).data
                    cart_exist.updated_on = datetime.datetime.now()
                    cart_exist.save()
                    return self.response(data={'item': item}, msg="done", status=True)

                else:

                    cart_items.update(qty=F('qty')+1)
                    already_added = CartAddCartItemSerializer(cart_items.first(),read_only=True).data
                    cart_exist.updated_on = datetime.datetime.now()
                    cart_exist.save()
                    return self.response(data={'item': already_added}, msg="Item already exists. Updating quantity.",status=True)


            item_data = Inventory.objects.filter(shop_id=shop_id, id=inventory_id)
            if item_data is None:
                return self.response(data=[], msg="Item does not exits", status=False)
            shop_exist = Shop.objects.filter(id=shop_id)

            if shop_exist.count() == 0:
                return self.response(data=[], msg="Shop does not exists", status=False)

            # cart_item_exist = Cartitem.objects.filter(shop_id=shop_id, cart_id=cart_id, inventory_id=inventory_id)
            # if cart_item_exist.count() > 0:
            #     already_added = Cartitem.objects.filter(id=cart_item_exist.first().id)
            #     already_added.update(qty=F('qty')+1)
            #     already_added = CartAddCartItemSerializer(already_added.first(),read_only=True).data
            #     return self.response(data={'item': already_added}, msg="Item already exists. Updating quantity.",status=True)
            # else:
            #     item = Cartitem.objects.create(qty=int(qty), cart=cart_exist.first(),inventory=item_data.first(),shop_id=shop_id)
            #     item = CartAddCartItemSerializer(item,read_only=True).data
            #     return self.response(data={'item': item}, msg="done", status=True)
        except Exception as ex:
            response = self.response(data=[], status=False, msg="something wrong")

        # try:
        #     cart_exist = Cart.objects.filter(id=cart_id)
        #     if cart_exist.count() == 0:
        #         return self.response(data=[], msg="cart does not exits", status=False)
        #     item_data = Inventory.objects.filter(shop_id=shop_id, id=inventory_id)
        #     if item_data is None:
        #         return self.response(data=[], msg="Item does not exits", status=False)
        #     shop_exist = Shop.objects.filter(id=shop_id)
        #
        #     if shop_exist.count() == 0:
        #         return self.response(data=[], msg="Shop does not exists", status=False)
        #
        #     cart_item_exist = Cartitem.objects.filter(shop_id=shop_id, cart_id=cart_id, inventory_id=inventory_id)
        #     if cart_item_exist.count() > 0:
        #         already_added = Cartitem.objects.filter(id=cart_item_exist.first().id)
        #         already_added.update(qty=F('qty')+1)
        #         already_added = CartAddCartItemSerializer(already_added.first(),read_only=True).data
        #         return self.response(data={'item': already_added}, msg="Item already exists. Updating quantity.",status=True)
        #     else:
        #         item = Cartitem.objects.create(qty=int(qty), cart=cart_exist.first(),inventory=item_data.first(),shop_id=shop_id)
        #         item = CartAddCartItemSerializer(item,read_only=True).data
        #         return self.response(data={'item': item}, msg="done", status=True)
        # except Exception as ex:
        #     response = self.response(data=[], status=False, msg="something wrong")
        return response