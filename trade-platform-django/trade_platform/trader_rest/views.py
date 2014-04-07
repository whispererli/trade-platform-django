import json
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics

from .models import ProductCatalog
from .models import ProductCatalogItem
from .models import UserAddress
from .models import UserOrder
from .models import UserProfile
from .serializers import AddressSerializer
from .serializers import MakeOrderExtraInfoSerializer
from .serializers import MakeOrderSerializer
from .serializers import ProductCatalogItemSerializer
from .serializers import ProductCatalogSerializer
from .serializers import UserOrderSerializer
from .serializers import UserSerializer


logger = logging.getLogger('trader_rest')

class UserList(generics.ListCreateAPIView):
    queryset  = UserProfile.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user profile instance.
    """
    queryset  = UserProfile.objects.all()
    serializer_class = UserSerializer
    
class AddressList(generics.ListCreateAPIView):
    queryset  = UserAddress.objects.all()
    serializer_class = AddressSerializer

class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user address instance.
    """
    queryset  = UserAddress.objects.all()
    serializer_class = AddressSerializer
    
class ProductCatalogList(generics.ListCreateAPIView):
    queryset  = ProductCatalog.objects.all()
    serializer_class = ProductCatalogSerializer

class ProductCatalogDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user address instance.
    """
    queryset  = ProductCatalog.objects.all()
    serializer_class = ProductCatalogSerializer

class ProductCatalogItemList(generics.ListCreateAPIView):
    queryset  = ProductCatalogItem.objects.all()
    serializer_class = ProductCatalogItemSerializer

class ProductCatalogItemDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user address instance.
    """
    queryset  = ProductCatalogItem.objects.all()
    serializer_class = ProductCatalogItemSerializer
    
class UserOrderList(generics.ListCreateAPIView):
    queryset  = UserOrder.objects.all()
    serializer_class = UserOrderSerializer
# request example
# {
#     "order": {
#         "expect_date": "2014-03-12",
#         "description": "order description",
#         "expect_price": "$123.11",
#         "product_catalog": "8",
#         "order_address": "3",
#         "uid": "2"
#     },
#     "extraInfo": [
#         {
#             "item": 1,
#             "item_value": "Cartier"
#         },
#         {
#             "item": 2,
#             "item_value": "No.011"
#         }
#     ]
# }
@csrf_exempt
def user_order_details(request): 
    if request.method == 'POST':
        req_json=json.loads(request.body)
        logger.info('REQUEST:=>')
        logger.info(req_json)
        order_serializer = MakeOrderSerializer(data=req_json['order'])
        if order_serializer.is_valid():
            order = order_serializer.save()
            for item in req_json['extraInfo']:
                item['order']=order.pk
            extra_info_serializer = MakeOrderExtraInfoSerializer(data=req_json['extraInfo'], many=True)
            if extra_info_serializer.is_valid():
                extra_info_serializer.save()
                return HttpResponse(200)
        return HttpResponse(500)