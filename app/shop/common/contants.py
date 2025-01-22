MRP_UPDATE_CSV_FILE_HEADERS = [
    "SKU",
    "Variant_Name",
    "MRP"
]
INVENTORY_UPDATE_CSV_FILE_HEADERS = [
    "SKU",
    "Name",
    "Category_Name",
    "Price",
    "MRP",
    "Status"
]
PRODUCT_CSV_FILE_HEADERS = ['Product_name','Category','Description','Manufacturer','Product_Image']


# PRODUCT_VARIANT_CSV_FILE_HEADERS = [
#     'Shop_Id','Product_id' ,'Shop_SKU','Variant_Name','SKU' ,'MRP' ,'Description','Weight','Variant_Image','Price']
PRODUCT_VARIANT_CSV_FILE_HEADERS = [
    'Shop_Id','Product_Name' ,'Variant_Name','Weight','Category_Name' ,'SKU' ,'Weight_In_Kg','Description','MRP','Price','Product_Image_URL','Variant_Image_URL'
]

MERCHANT_INVENTORY_BULK_UPDATE = ['inventory_id', 'variant_name', 'product_name', 'shop_id', 'shop_name', 'shop_sku', 'category',
                                  'price', 'mrp',
                                  'status']

MESSAGES = {
    "MRP_LESS_THAN_PRICE": "MRP should be greater than or equal to selling price.",
    "SIGNATURE_VERIFICATION_FAILED":"Failed to Verify CashFree Signature ",
    "DONE": "Done",
    "USER_BLOCKED":"Your Account Has Been Blocked , Please Contact Administrator",
    "NO_ACCESS" : "You have No permission to do this Action",
    "FAILED": "Failed",
    "PRODUCT_NOT_EXIST":"This Product does not exist",
    "PRODUCT_VARIANT_NOT_EXIST":"Product Variant for given id does not exist",
    "PRODUCT_NAME_ALREADY_EXIST":"Given Product name is already exist",
    "ERP_INVOICE_NOT_GENERATED": "Invoice is not generated. Please try again later.",
    "PRODUCT_SKU_ALREADY_EXISTS": "SKU already exists.",
    "ATLEAST_ONE_ATTRIBUTE": "Variant need atleast one attribute.",
    "PRODUCT_ATTRIBUTE_NAME_ALREADY_EXISTS": "Attribute combination of name, unit and value already exists.",
    "INVALID_CREDENTIALS": "Invalid Username or Password",
    "INVALID_DATA": "Invalid Data",
    "PRODUCT_MRP_LESS_THAN_MAX_PRICE": "MRP should be greater than or equal to selling price.",
    "INSUFFICIENT_DATA": "Data not valid.",
    "INVALID_CSV": "Invalid CSV file. Please ensure data has been entered and headers are valid.",
    "UPLOAD_COMPLETED": "Upload Completed",
    "EMPTY_CSV": "CSV is empty.",
    "ERROR_IN_CSV": "Some errors in the CSV",
    "INVALID PAGE": "Invalid page.",
    "UNAUTHORIZED": "Unauthorized",
    "USER_EXISTS": "User already exists with the given details.",
    "FORCE_CREATION": "User force updated to merchant",
    # "PHONE_NUMBER_EXISTS_TRY_FORCE_CREATION": "User with this phone number already exists. pass force_creation=true to remap as merchant",
    "PHONE_NUMBER_EXISTS_TRY_FORCE_CREATION": "User with this phone number already exists",
    "MERCHANT_DISABLED": "Your Account is Blocked. Please contact Administrator",
    "MERCHANT_DELETION_FAILED": "something broke",
    "USER_DELETION_FAILED" : "User Deletion Failed",
    "USER_ENABLED_FAILED" : "User Enabling Failed",
    "MERCHANT_UPDATE": "Merchant updated",
    "USER_UPDATE": "User updated",
    "NO_USER": "User doesn't exists",
    "PASS_ID_TO_UPDATE_MERCHANT": "Pass the id parameter to update a merchant",
    "PASS_ID_TO_UPDATE_USER": "Pass the id parameter to update a user",
    "EMAIL_EXISTS": "Email is already exists",
    "PHONE_EXISTS": "Phone number is already exists",
    "PRIORITY_EXISTS": "Priority already exists",
    "DISABLE_SHOPS": "Please disable enabled shops and retry",
    "DATA_NOT_VALID": "Data not valid.",
    "INVALID_REQUEST": "Invalid request",
    "INVALID_PARAMS": "invalid params",
    "NO_ORDER": "Order not found",
    "NO_DATA": "data not found",
    "NO_SHOP": "shop does not exist",
    "NO_ROUTE": "Couldn't find the route. Please choose an alternate pickup or delivery location.",
    "INVALID_WEIGHT": "Weight should be greater than zero",
    "NO_REGION": "Region not found",
    "NO_PERMISSION": "No permission to do this operation",
    "PRODUCT_REMOVE": "Product removed successfully",
    "VARIANT_REMOVE": "Variant removed successfully",
    "PROMOTION_EXISTS": "Promotion code already exists",
    "PRODUCT_PRICE_LESS_THAN_OR_EQUAL_MRP": "Price should be less than or equal to MRP and Greater than Zero.",
    "INVALID_PRODUCT": "Provide valid shop name and product name",
    "PRODUCT_NOT_FOUND": "Product is not found for the corresponding shop",
    "NOT_ALLOWED": "You have no permission to modify this product",
    "INVALID_START_TIME": "Invalid start time",
    "INVALID_END_TIME": "Invalid end time",
    "NOT_VALID_STATUS": "Not a valid status(status must be Enabled or Disabled)",
    "PRIORITY_NOT_NEGATIVE": "Not allowing negative values to priority",
    "PRIORITY_EXIST": "Priority already exist",
    "CATEGORY_NAME_EXIST": "Category already exists with this name.",
    "START_GREATER_THAN_END": "Shop Working Time should be valid",
    "SHOP_SKU_ALREADY_EXISTS": "Shop SKU already exists.",
    "SHOP_SKU_IS_MANDATORY": "Shop SKU is Mandatory.",
    "CSV_GENERATED": "Your request for CSV download is in-progress. Please visit the reports download page to download "
                     "the report.",
    "CANNOT_MODIFY_WALLET_ORDER": "Promo code applied wallet order cannot be modified.",
    "PRODUCT_NEED_ATLEAST_ONE_VARIANT":"Product need atleast one variant",
    "INVALID_SHOP_ID": "Invalid shop ID. Please provide a valid shop ID",
    "PUBLIC_PRODUCT_EXIST_INVENTORY":"Public Product already added in Inventory",
    "PRIVATE_PRODUCT_EXIST_INVENTORY": "Private Product already added in for other shop merchant",
    "WEIGHT_REQUIRED":"Weight is Mandatory for Variant",
    "DISABLED_MERCHANT" : "Shop can't be enabled. Enable the merchant and try again.",
    "SHOP_SKU_MANDATORY":"Shop sku is mandatory",
    "SHOP_NOT_AVAILABLE":"Shop is not available during the specified time range"

}

CART_STATUS = {
    "NEW": "new",
    "TRANSACTION INITIATED": 'transaction initiated',
    "CHECKED_OUT": 'checked out',
    "REMOVED": 'removed'
}
USER = {
    'ADMIN': 1,
    'MERCHANT': 2,
    'STAFF': 3,
    'USER': 4
}
ORDER_STATUS = {
    'PaymentDone': 'PaymentDone',
    'PaymentPending': 'PaymentPending',
    'PaymentFailed': 'PaymentFailed',
    'Placed': 'Placed',
    'Approved': 'Approved',
    'Rejected': 'Rejected',
    'Modified': 'Modified',
    'Packed': 'Packed',
    'AwaitingPickUp': 'AwaitingPickUp',
    'DriverAccepted': 'DriverAccepted',
    'Enroute': 'Enroute',
    'Delivered': 'Delivered',
    'CancelledCustomer': 'CancelledCustomer',
    'CancelledMerchant': 'CancelledMerchant',
    'CancelledQwqer': 'CancelledQwqer',
    'Undelivered': 'Undelivered'
}
ORDER_PAYMENT_TYPE = {
    'COD': 1,
    'OnlinePayment': 2,
    'Wallet': 3
}