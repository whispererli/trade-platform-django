'''
Created on Apr 1, 2014

@author: m68li
'''
#from django.core import serializers as djangoSerializers
import json
import logging

from rest_framework import serializers

from .models import OrderTopics
from .models import ProductCatalog
from .models import ProductCatalogItem
from .models import TopicComments
from .models import UserAddress
from .models import UserOrder
from .models import UserOrderExtraInfo
from .models import UserProfile


logger = logging.getLogger('trader_rest')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('uid', 'address1', 'address2','city', 'nation', 'post')
        write_only_fields  = ('uid',)

class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True)
    class Meta:
        model = UserProfile
        fields = ('id', 'gender', 'name', 'birthday','email', 'phone', 'description', 'address', 'regist_date')
        write_only_fields  = ('user_pw', )
        read_only_fields  = ('id', 'regist_date')

class ProductCatalogItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCatalogItem
        fields = ('id', 'product_catalog', 'item_name','item_required')
        write_only_fields  = ('product_catalog',)
        read_only_fields  = ('id',)
class ProductCatalogSerializer(serializers.ModelSerializer):
    catalog_items = ProductCatalogItemSerializer(many=True)
    class Meta:
        model = ProductCatalog
        fields = ('id','product_catalog_name','catalog_items')
        read_only_fields  = ('id',)
        

class OrderExtraInfoSerializer(serializers.ModelSerializer):
    item_content = ProductCatalogItemSerializer()
    item = ProductCatalogItemSerializer()
    class Meta:
        model = UserOrderExtraInfo
        fields = ('order','item', 'item_value',)

class TopicCommentsSerializer(serializers.ModelSerializer):
    tid = serializers.PrimaryKeyRelatedField()
    class Meta:
        model = TopicComments
        fields = ('tid','comment','comment_time')
        read_only_fields  = ('comment_time',)
        
class OrderTopicsSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField()
    uid = serializers.PrimaryKeyRelatedField()
    topiccomments_set = TopicCommentsSerializer(many=True, required=False)
    class Meta:
        model = OrderTopics
        fields = ('id','order_id','uid','topiccomments_set')
        read_only_fields  = ('id',)
    def save_object(self, obj, **kwargs):
        super(OrderTopicsSerializer, self).save_object(obj, **kwargs)
        return obj       
class UserOrderSerializer(serializers.ModelSerializer):
    uid = UserSerializer()
    order_address = AddressSerializer()
    userorderextrainfo_set = OrderExtraInfoSerializer(many=True)
    ordertopics_set = OrderTopicsSerializer(many=True)
    class Meta:
        model = UserOrder
        fields = ('id','expect_date','order_time', 'description','expect_price','product_catalog','order_address', 'userorderextrainfo_set','uid','ordertopics_set')
        read_only_fields  = ('id', 'order_time')
        
class MakeOrderExtraInfoSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField()
    item = serializers.PrimaryKeyRelatedField()
    class Meta:
        model = UserOrderExtraInfo
        fields = ('order','item', 'item_value')
class MakeOrderSerializer(serializers.ModelSerializer):
    uid = serializers.PrimaryKeyRelatedField()
    order_address = serializers.PrimaryKeyRelatedField()
    product_catalog = serializers.PrimaryKeyRelatedField()
    class Meta:
        model = UserOrder
        fields = ('expect_date','description','expect_price','product_catalog','order_address','uid')
    def save_object(self, obj, **kwargs):
        super(MakeOrderSerializer, self).save_object(obj, **kwargs)
        return obj