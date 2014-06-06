# -*- coding: utf-8 -*-
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


logger = logging.getLogger('trader_rest')  

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
#  用户信息表 
class UserProfile(models.Model):
    MALE, FEMALE = 'M', 'F'
    GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'))
    user = models.OneToOneField(User, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                              verbose_name='Gender', null=True)
    birthday = models.DateField(null=True)
#   Optional
    name = models.CharField(max_length=20,null=True)
    phone = models.CharField(max_length=20,null=True)
    description = models.CharField(max_length=500,null=True)
    profile_image = models.CharField(max_length=50,null=True)
#     def save(self, *args, **kwargs):       
#         #create user in django
#         try:
#             django_user = User.objects.get(username=self.email)
#         except (User.DoesNotExist):
#             django_user = None
#         if django_user is None:
#             django_user = User.objects.create_user(self.email, self.email, self.user_pw)
#             Token.objects.create(user=django_user)
#             super(UserProfile, self).save(*args, **kwargs) # Call the "real" save() method.
#         else:
#             logger.error('User already exsit.')

#  地址表 
class UserAddress(models.Model):
    uid  = models.ForeignKey(User, related_name='address') # Many-to-one User profile
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, null=True)
    city  = models.CharField(max_length=10)
    nation  = models.CharField(max_length=10)
    post = models.CharField(max_length=10)

#  用户登陆表 
class UserLogin(models.Model):
    uid = models.ForeignKey(User) # Many-to-one User
    last_login = models.DateTimeField(auto_now_add=True)
    device = models.CharField(max_length=100)
    ip = models.IPAddressField(max_length=20)

#  产品类别表 例：服装，食品，奢饰品
class ProductCatalog(models.Model):
    product_catalog_name = models.CharField(max_length=20)

#  产品类别明细表
class ProductCatalogItem(models.Model):
    item_name = models.CharField(max_length=100)
    item_required = models.BooleanField()
    product_catalog = models.ForeignKey(ProductCatalog, related_name='catalog_items') # Many-to-one productCatalog

#  用户订单表
class UserOrder(models.Model):
    PREPARE, ACTIVE, FINISH, CANCEL = 'P', 'A', 'F', 'C'
    STATUS_CHOICES = (
    (PREPARE, 'Preparing'),
    (ACTIVE, 'Active'),
    (FINISH, 'Finish'),
    (CANCEL, 'Cancelled'))
    
    expect_date = models.DateField()
    order_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500)   
    expect_price = models.CharField(max_length=10)
    order_status = models.CharField(max_length=1, choices=STATUS_CHOICES,
                            verbose_name='OrderStatus')
    uid = models.ForeignKey(User)
    product_catalog = models.ForeignKey(ProductCatalog)
    order_address = models.ForeignKey(UserAddress)

# 订单图片表？产品图片表？
class OrderImage(models.Model):
    order_id = models.ForeignKey(UserOrder, related_name='order_images')
    path = models.FilePathField()

#  用户订单额外信息表 
class UserOrderExtraInfo(models.Model):
    order = models.ForeignKey(UserOrder)
    item = models.ForeignKey(ProductCatalogItem)
    item_value = models.CharField(max_length=100)

#  订单评论表   
class OrderTopics(models.Model):
    order_id = models.ForeignKey(UserOrder)
    uid = models.ForeignKey(User)

#  用户评论表
class TopicComments(models.Model):
    tid = models.ForeignKey(OrderTopics)
    comment = models.CharField(max_length=500)
    comment_time = models.DateTimeField(auto_now_add=True)

#  报价表 
class UserrQuote(models.Model):
    order_id = models.ForeignKey(UserOrder, related_name='order_quote')
    uid = models.ForeignKey(User)
    expect_price = models.CharField(max_length=10)
    valid_time = models.DateTimeField()

