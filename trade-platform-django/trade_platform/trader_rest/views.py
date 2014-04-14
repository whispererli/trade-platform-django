import json
import logging

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view

from .models import OrderTopics
from .models import ProductCatalog
from .models import ProductCatalogItem
from .models import UserAddress
from .models import UserOrder
from .models import UserProfile
from .serializers import AddressSerializer
from .serializers import MakeOrderExtraInfoSerializer
from .serializers import MakeOrderSerializer
from .serializers import OrderTopicsSerializer
from .serializers import ProductCatalogItemSerializer
from .serializers import ProductCatalogSerializer
from .serializers import TopicCommentsSerializer
from .serializers import UserOrderSerializer
from .serializers import UserProfileSerializer
from .serializers import UserSerializer


logger = logging.getLogger('trader_rest')

class UserList(generics.ListCreateAPIView):
    queryset  = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update a user profile instance.
    """
    queryset  = User.objects.all()
    serializer_class = UserSerializer

class UserProfileList(generics.ListCreateAPIView):
    queryset  = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update a user profile instance.
    """
    queryset  = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
class AddressList(generics.ListCreateAPIView):
    queryset  = UserAddress.objects.all()
    serializer_class = AddressSerializer

class AddressDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update a user address instance.
    """
    queryset  = UserAddress.objects.all()
    serializer_class = AddressSerializer
    
class ProductCatalogList(generics.ListCreateAPIView):
    queryset  = ProductCatalog.objects.all()
    serializer_class = ProductCatalogSerializer

class ProductCatalogDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update a user address instance.
    """
    queryset  = ProductCatalog.objects.all()
    serializer_class = ProductCatalogSerializer

class ProductCatalogItemList(generics.ListCreateAPIView):
    queryset  = ProductCatalogItem.objects.all()
    serializer_class = ProductCatalogItemSerializer

class ProductCatalogItemDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update a user address instance.
    """
    queryset  = ProductCatalogItem.objects.all()
    serializer_class = ProductCatalogItemSerializer

@api_view(['POST'])
def make_comment(request): 
    req_json=json.loads(request.body)
    logger.info('%s:%s' % ('REQUEST BODY', req_json))
    try:
        topic = OrderTopics.objects.get(pk=req_json['topic'])
    except (OrderTopics.DoesNotExist,KeyError):
        logger.info('Topic not found.')
        topic = None
    if topic is None:
        topic_serializer = OrderTopicsSerializer(data={'order_id':req_json['comment']['order_id'],'uid':request.user.pk})
        if topic_serializer.is_valid():
            topic = topic_serializer.save()
    
    req_json['comment']['tid'] = topic.pk
    comment_serializer = TopicCommentsSerializer(data=req_json['comment'])
    if comment_serializer.is_valid():
        comment_serializer.save()
        return HttpResponse()
    return HttpResponse(status=500)

class UserOrderList(generics.ListAPIView):
    queryset  = UserOrder.objects.all()
    serializer_class = UserOrderSerializer
        
class UserOrderListByFilter(generics.ListAPIView):
    serializer_class = UserOrderSerializer
    def get_queryset(self):
        queryset = UserOrder.objects.all()
        #filter by user id
        return UserOrder.objects.filter(uid=self.request.user.pk)
        #filter by catalog
        catalog = self.request.QUERY_PARAMS.get('catalog', None)
        if catalog is not None:
            return queryset.filter(product_catalog=catalog)
        #filter by date range
        from_date = self.request.QUERY_PARAMS.get('fromdate', None)
        to_date = self.request.QUERY_PARAMS.get('todate', None)
        if from_date is not None and to_date is not None:
            return queryset.filter(expect_date_at__range=(from_date, to_date))
        #filter by address, need to change address structure...
        # no filter
        return queryset
        
#TODO: should implement avro later
# make_order request example
# {
#     "order": {
#         "expect_date": "2014-03-12",
#         "description": "order description",
#         "expect_price": "$123.11",
#         "product_catalog": "8",
#         "order_address": "3"
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
@api_view(['POST'])
def make_order(request):
    req_json=json.loads(request.body)
    logger.info('%s:%s' % ('REQUEST BODY', req_json))
    logger.info(req_json)
    req_json['order']['uid']=request.user.pk
    order_serializer = MakeOrderSerializer(data=req_json['order'])
    if order_serializer.is_valid():
        order = order_serializer.save()
        for item in req_json['extraInfo']:
            item['order']=order.pk
        extra_info_serializer = MakeOrderExtraInfoSerializer(data=req_json['extraInfo'], many=True)
        if extra_info_serializer.is_valid():
            extra_info_serializer.save()
            return HttpResponse(200)
    return HttpResponse(status=500)