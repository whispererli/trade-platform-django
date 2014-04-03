# -*- coding: utf-8 -*-

from django.db import models


#  用户信息表 
# CREATE TABLE user_tbl
# (
#   uid                  BIGINT UNSIGNED        NOT NULL AUTO_INCREMENT,
#   email                VARCHAR(255)           NOT NULL,
#   user_pw              VARCHAR(255)           NOT NULL,
#   birthday             DATE                   NOT NULL,  
#   gender               ENUM('M', 'F')         NOT NULL, -- male, female
#   regist_date          DATE                   NOT NULL,
#   permission           ENUM('A', 'U')         NOT NULL,  -- admin, user
#   
#   -- fill in later
#   name                 VARCHAR(255)           ,
#   phone                CHAR(20)               ,
#   addr_id              BIGINT UNSIGNED        ,
#   description          VARCHAR(255)           ,
# 
#   PRIMARY KEY (uid),
#   UNIQUE KEY (uid, email),
#   INDEX IDX_BY_EMAIL(email)
# );
# 
class UserProfile(models.Model):
    MALE, FEMALE = 'M', 'F'
    GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'))
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                              verbose_name='Gender')
    birthday = models.DateField()
    email = models.EmailField()
    user_pw = models.CharField(max_length=20)
    regist_date = models.DateTimeField(auto_now_add=True)  
#   Optional
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)  
    description = models.CharField(max_length=500)

#  地址表 
# CREATE TABLE user_addr_tbl
# (
#   uid                 BIGINT UNSIGNED NOT NULL ,
#   addr_id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
#   address             VARCHAR(255)    NOT NULL,
#   city                VARCHAR(255)    NOT NULL,
#   nation              VARCHAR(255)    NOT NULL,
#   post                VARCHAR(20)     NOT NULL,
#   PRIMARY KEY (addr_id),
#   UNIQUE KEY (uid, addr_id)
# );
class UserAddress(models.Model):
    uid  = models.ForeignKey(UserProfile, related_name='address') # Many-to-one User profile
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city  = models.CharField(max_length=10)
    nation  = models.CharField(max_length=10)
    post = models.CharField(max_length=10)
    def __unicode__(self):
        return self.address1, self.address2, self.city, self.nation, self.post
#  用户登陆表 
# CREATE TABLE user_login_tbl
# (
#   uid                  BIGINT UNSIGNED NOT NULL,
#   last_login           DATE            NOT NULL,
#   last_logout          DATE            NOT NULL,
#   device               VARCHAR(50)    NOT NULL, 
#   ip                   VARCHAR(20)     NOT NULL,
#   FOREIGN KEY (user_login_tbl_uid) REFERENCES user_tbl(uid),
#   INDEX IDX_BY_UID(uid)
# );
class UserLogin(models.Model):
    uid = models.ForeignKey(UserProfile) # Many-to-one User profile
    last_login = models.DateTimeField()
    device = models.CharField(max_length=100)
    ip = models.IPAddressField(max_length=20)

# 
#  产品类别表 例：服装，食品，奢饰品
# CREATE TABLE product_catalog_tbl
# (
#   catalog_id               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
#   product_catalog_name     VARCHAR(255)    NOT NULL,
#   PRIMARY KEY (product_id)
# );
class ProductCatalog(models.Model):
    product_catalog_name = models.CharField(max_length=20)

#  产品类别明细表 
# CREATE TABLE product_catalog_item_tbl
# (
#   item_id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
#   item_name            VARCHAR(255)    NOT NULL,
#   item_required        BOOLEAN         NOT NULL,
#   PRIMARY KEY (item_id) 
# );
# 
#  产品类别与明细关系表 
# CREATE TABLE product_catalog_item_map_tbl
# (
#   catalog_id       BIGINT UNSIGNED    NOT NULL,
#   item_id          BIGINT UNSIGNED    NOT NULL,
#   UNIQUE KEY (catalog_id, item_id), 
#   FOREIGN KEY (product_catalog_item_map_tbl_catalog_id)  REFERENCES product_catalog_tbl(catalog_id),
#   FOREIGN KEY (product_catalog_item_map_tbl_item_id) REFERENCES product_catalog_item_tbl(item_id),
#   INDEX IDX_BY_CATALOG_ITEM(catalog_id, item_id)
# );
class ProductCatalogItem(models.Model):
    item_name = models.CharField(max_length=100)
    item_required = models.BooleanField()
    product_catalog = models.ForeignKey(ProductCatalog, related_name='catalog') # Many-to-one productCatalog

#  用户订单表 
# CREATE TABLE user_order_tbl
# (
#   order_id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
#   uid                  BIGINT UNSIGNED NOT NULL,
#   expect_time          DATE            NOT NULL,
#   order_time           DATE            NOT NULL,
#   description          VARCHAR(255)    NOT NULL,
#   catalog_id           BIGINT UNSIGNED NOT NULL,
#   expect_price         VARCHAR(255)    NOT NULL,
#   addr_id              VARCHAR(255)    NOT NULL,
#   FOREIGN KEY (user_order_tbl_uid) REFERENCES user_tbl(uid),
#   FOREIGN KEY (user_order_tbl_catalog_id)  REFERENCES product_catalog_tbl(catalog_id),
#   FOREIGN KEY (user_order_tbl_addr_id)  REFERENCES user_addr_tbl(addr_id),
#   PRIMARY KEY (order_id)
# );
# 
class UserOrder(models.Model):
    uid = models.ForeignKey(UserProfile)
    expect_date = models.DateField()
    order_time = models.DateTimeField()
    description = models.CharField(max_length=500)
    product_catalog = models.ForeignKey(ProductCatalog, related_name='order_catalog')
    expect_price = models.CharField(max_length=10)
    order_address = models.ForeignKey(UserAddress, related_name='order_addr')

# 订单图片表？产品图片表？
class OrderImage(models.Model):
    order_id = models.ForeignKey(UserOrder, related_name='order_images')
    path = models.FilePathField()

#  用户订单额外信息表 
# CREATE TABLE user_order_catalog_item_map_tbl
# (
#   order_id         BIGINT UNSIGNED    NOT NULL,
#   catalog_id       BIGINT UNSIGNED    NOT NULL,
#   item_id          BIGINT UNSIGNED    NOT NULL,
#   item_value       BLOB               NOT NULL,  -- photo, text, number, etc
#   FOREIGN KEY (user_order_catalog_item_map_tbl_order_id) REFERENCES user_order_tbl(order_id),
#   FOREIGN KEY (user_order_catalog_item_map_tbl_catalog_id)  REFERENCES product_catalog_tbl(catalog_id),
#   FOREIGN KEY (user_order_catalog_item_map_tbl_item_id) REFERENCES product_catalog_item_tbl(item_id),
#   UNIQUE KEY (order_id, catalog_id, item_id)
# );
# 
class UserOrderExtraInfo(models.Model):
    order_id = models.ForeignKey(UserOrder, related_name='order_extra_info')
    item_id = models.ForeignKey(ProductCatalogItem, related_name='order_items')
    item_value = models.CharField(max_length=100)

#  用户订单评论表 
# CREATE TABLE user_order_comments_tbl
# (
#   order_id             BIGINT UNSIGNED NOT NULL,
#   uid                  BIGINT UNSIGNED NOT NULL,
#   user_comment         VARCHAR(255)    NOT NULL,
#   comment_time         DATE            NOT NULL,
#   FOREIGN KEY (user_order_comments_tbl_uid) REFERENCES user_tbl(uid),
#   FOREIGN KEY (user_order_comments_tbl_order_id) REFERENCES user_order_tbl(order_id)
# );
class OrderComments(models.Model):
    order_id = models.ForeignKey(UserOrder)
    uid = models.ForeignKey(UserProfile)
    comment = models.CharField(max_length=500)
    comment_time = models.DateTimeField(auto_now_add=True)
# 
#  报价表 
# CREATE TABLE user_quote_tbl
# (
#   order_id            BIGINT UNSIGNED NOT NULL,
#   uid                 BIGINT UNSIGNED NOT NULL,
#   expect_price        VARCHAR(255)    NOT NULL,
#   valid_time          DATE            NOT NULL,
#   FOREIGN KEY (user_quote_tbl_order_id) REFERENCES user_order_tbl(order_id),
#   FOREIGN KEY (user_quote_tbl_uid) REFERENCES user_tbl(uid)
# );
class UserrQuote(models.Model):
    order_id = models.ForeignKey(UserOrder, related_name='order_quote')
    uid = models.ForeignKey(UserProfile)
    expect_price = models.CharField(max_length=10)
    valid_time = models.DateTimeField()

