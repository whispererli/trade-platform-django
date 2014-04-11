'''
Created on Apr 1, 2014

@author: m68li
'''
#from django.core import serializers as djangoSerializers
import logging

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField()
    class Meta:
        model = UserProfile
        fields = ('id', 'gender', 'name', 'birthday', 'phone', 'description', 'user')
        read_only_fields  = ('id',)
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username','password','is_active','is_staff','date_joined')
        read_only_fields  = ('id','is_active','is_staff', 'date_joined')
    def restore_object(self, attrs, instance=None):
        if instance is None:
            """
            Instantiate a new User instance.
            """
            user = User(email=attrs['email'], username=attrs['email'])
            user.set_password(attrs['password'])
        else:
            instance.email=attrs['email']
            instance.username=attrs['email']
            instance.password=attrs['password']
            return instance
        return user

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