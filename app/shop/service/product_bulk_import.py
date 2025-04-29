import pandas as pd
import os
from datetime import datetime
import re
pattern = re.compile(r'\b(\d+)\s+([a-zA-Z]+)\b')
from django.db.models import Prefetch,Q
import re
from ..models import Inventory,Shop
from product.models import ProductVariant,Product,ProductAttributeVariant,ProductAttribute

from category.models import Category
from ..common import PRODUCT_VARIANT_CSV_FILE_HEADERS

class ProductCSVBulkCreateService:
    field_names =''
    @classmethod
    def validate_csv(self, data):
        csv_data = pd.read_csv(data["file"], )
        validate_status = self.validate_header(csv_data)
        csv_empty_check = self.csv_empty_check(csv_data) if validate_status else None
        filename, file_extension = os.path.splitext(data["file"].name)

        validate_status = True if file_extension.strip().upper() == ".CSV" else False
        if validate_status:
            return True, csv_data, csv_empty_check
        else:
            return False, csv_data, csv_empty_check

    @classmethod
    def csv_empty_check(self, csv_data):
        row_list = csv_data.values.tolist()
        rows = [self.format_row_data(row) for row in row_list]
        if row_list == [] or rows == []:
            return True
        else:
            return False

    @classmethod
    def validate_header(self, csv_data):

        self.field_names = PRODUCT_VARIANT_CSV_FILE_HEADERS
        header_check_list = []

        headers = csv_data.columns.values.tolist()
        for header in headers:
            if header[-1] == '*':
                header = header[:-1]
            header_check_list.append(header)
        if header_check_list[:len( self.field_names)] ==  self.field_names:
            return True
        else:
            return False

    @classmethod
    def process_csv(self, csv_data,user,action=''):
        error = []
        row_list = [self.format_row_data(row) for row in csv_data.values.tolist()]

        if action == 'create':
            error = self.add_product_variant(row_list)

        return error

    @classmethod
    def format_row_data(self, row):
        data = {}
        i = 0
        all_empty = True  # if all values in the row are empty
        for key in self.field_names:
            val = row[i]
            val = "" if str(val) == "nan" else val
            if val:
                all_empty = False
            data[i] = val
            i = i + 1
        return data if not all_empty else None

    @classmethod
    def validate_string_length(self,s, min_length, max_length):
        if min_length <= len(s) <= max_length:
            return True
        else:
            return False


    @classmethod
    def add_product_variant(self, row_list, is_private=False, merchant_id='',user=None):
        error = []

        for row in row_list:
            try:

                product = ''
                variant =''
                row,attribute,merchant_id    = self.basic_csv_validation(row)
                if not row[12]:
                    if not ProductVariant.objects.filter(sku=row[5], is_deleted=False).exists():
                        if not self.validate_string_length(row[7],0,50):
                            row[12] = "Product Description does not exceed  more than 50 characters ." if \
                                row[12] == '' else row[12] + ';' + "Product Description does not exceed more than 50 characters . ."
                        else:
                            row, product = self.product_create(row, merchant_id, user)

                        if not row[12]:
                            row,variant = self.create_variant(row,product,user,attribute)

                    else:
                        variant =  ProductVariant.objects.filter(sku=row[5]).first()
                        product =  Product.objects.filter(id=variant.product_id).first()

                if not row[9]:
                    row[12] = "Price is mandatory ." if row[12] == '' else row[12] + ';' + "Price is mandatory ."

                elif not (isinstance(row[9], int) or isinstance(row[9], float)):
                    row[12] = "Invalid Price ." if row[12] == '' else row[12] + ';' + "Invalid Price ."

                elif row[8] and (isinstance(row[8], int) or isinstance(row[8], float)) and row[9] > row[8]:
                    row[12] = "Price cannot exceeds MRP ." if row[12] == '' else row[12] + ';' + "Price cannot exceeds MRP ."


                if row[12]:
                    error.append(row)

                else:


                    self.create_inventory(row,product,variant,user)

            except Exception as ex:
                print("ProductCSVBulkCreateService process_csv", ex)
        return error

    @classmethod
    def basic_csv_validation(self,row):
        numeric_pattern = re.compile(r'^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$')
        attribute = ''
        merchant_id = ''

        row[12] = ''
        if not row[0]:
            row[12] = "Shop Id is Mandatory ."

        elif not (isinstance(row[0], int) or isinstance(row[0], float)):
            row[12] = "Invalid Shop Id ."

        elif not Shop.objects.filter(id=row[0]).exists():
            row[12] = "Shop does not exist corresponding Shop Id ."

        if not str(row[5]).strip():
            row[12] = "SKU is mandatory ." if row[12] == '' else row[12] + ';' + "SKU is Mandatory ."

        elif not isinstance(str(row[5]).strip(), str):
            row[12] = "Invalid SKU ." if row[12] == '' else row[12] + ';' + "Invalid SKU ."
        if not str(row[2]).strip():
            row[12] = "Variant Name is mandatory ." if row[12] == '' else row[
                                                                              12] + ';' + "Variant Name is mandatory ."
        if row[5] != '':
            if ProductVariant.objects.filter(Q(sku=str(row[5]).strip()) & ~Q(name=str(row[2]).strip())).exists():
                row[12] = "The Product-variant is for the given SKU is already Exist ." if row[12] == '' else \
                    row[12] + ';' + "The Product-variant is for the given SKU is already Exist."

        if not row[9]:
            row[12] = "MRP is mandatory ." if row[12] == '' else row[12] + ';' + "MRP is mandatory ."

        elif not (isinstance(row[8], int) or isinstance(row[8], float)):

            row[12] = "Invalid MRP ." if row[12] == '' else row[12] + ';' + "Invalid MRP ."

        if not row[1]:
            row[12] = "Product Name is Mandatory ." if row[12] == '' else row[
                                                                              12] + ';' + "Product Name is Mandatory ."
        elif  Product.objects.filter(name=str(row[1]).strip()) and Product.objects.filter(name=str(row[1]).strip()).first().is_deleted ==True:
            row[12] = "Product is Already Deleted ." if row[12] == '' else row[
                                                                              12] + ';' + "Product is Already Deleted ."

        if not row[4]:
            row[12] = "Product Category is Mandatory ." if row[12] == '' else row[
                                                                                  12] + ';' + "Product Category is Mandatory ."
        elif not isinstance(row[4], str):
            row[12] = "Invalid Product Category Name." if row[12] == '' else row[
                                                                                 12] + ';' + "Invalid Product Category Name."
        elif not Category.objects.filter(name=str(row[4]).strip()).exists():
            row[12] = "Product Category Does not Exist." if row[12] == '' else row[
                                                                                   12] + ';' + "Product Category Does not Exist."

        if row[10] and not isinstance(row[10], str):
            row[12] = "Need a valid file Id for product." if row[12] == '' else row[
                                                                                    12] + ';' + "Need a valid file Id for product."


        if not row[3]:
            row[12] = "Weight is mandatory ." if row[12] == '' else row[12] + ';' + "Weight is mandatory ."
        elif row[3] and not isinstance(row[3], str):
            row[12] = "Invalid Weight  ." if row[12] == '' else row[12] + ';' + "Invalid Weight ."

        elif not ProductAttribute.objects.filter(attribute_label=row[3]).exists():
            row[12] = "Weight attribute does not exist please request to admin to add new." if row[
                                                                                                   12] == '' else \
                row[
                    12] + ';' + "Weight attribute does not exist please request to admin to add new. ."
        else:
            attribute = ProductAttribute.objects.filter(attribute_label=row[3]).first()

        if not row[6]:
            row[12] = "Weight In Kg is mandatory ." if row[12] == '' else row[
                                                                              12] + ';' + "Weight In Kg is mandatory ."
        elif not numeric_pattern.match(str(row[6])):
            row[12] = "Invalid Weight In Kg ." if row[12] == '' else row[
                                                                         12] + ';' + "Invalid Weight In Kg."

        if not (row[10] or row[11]):
            row[12] = "Need a image either for product or product variant." if row[12] == '' else row[
                                                                                                      12] + ';' + "Need a image either for product or product variant."
        return row,attribute,merchant_id

    @classmethod
    def product_create(cls,row,merchant_id=None,user=None):
        product=''
        if not Product.objects.filter(name=str(row[1]).strip()).exists():
            pdt = {}
            category_obj = Category.objects.filter(name=str(row[4]).strip()).first()
            user = user
            pdt['category'] = category_obj
            pdt['created_user'] = user
            pdt['name'] = row[1]


            product = Product.objects.create(**pdt)
            # if row[12]:
            #     ProductImageUpload.upload_product_image_csv(row[12], product.id)


        else:

            product = Product.objects.filter(name=str(row[1]).strip()).first()

        return row,product

    @classmethod
    def create_variant(cls,row,product,user,attribute):
        variant_details = {}
        variant_details['product_id'] = product.id
        variant_details['sku'] = str(row[5]).strip()

        variant_details['mrp'] = row[8]
        variant_details['name'] = str(row[2]).strip()
        variant_details['weight'] = row[6]
        variant_details['unit'] = 'KG'
        variant_details['description'] = row[7]
        variant_details['is_deleted'] = False

        variant_details['created_at'] = datetime.utcnow()
        variant_details['created_user'] = user

        variant = ProductVariant.objects.create(**variant_details)
        ProductAttributeVariant.objects.create(variant_id=variant.id, attribute_id=attribute.id)
        # if row[13]:
        #     ProductImageUpload.upload_product_image_csv(row[13], product.id, variant.id)
        return row,variant
    @classmethod
    def create_inventory(cls,row,product,variant,user):
        inventory = Inventory.objects.filter(is_deleted=False, shop_id=row[0], product_variant=variant).first()

        if not inventory:
            inventory_details = {}
            inventory_details['product_id'] = product.id
            inventory_details['product_variant_id'] = variant.id
            inventory_details['shop_id'] = row[0]
            inventory_details['created_at'] = datetime.utcnow()

            inventory_details['price'] = row[9]
            inventory_details['priority'] = 0
            inventory_details['is_enabled'] = True
            inventory_details['is_scheduled'] = False
            inventory_details['created_user'] = user

            inventory = Inventory.objects.create(**inventory_details)
            inventory = Inventory.objects.filter(id=inventory.id).select_related('product', 'product__category').first()

