from django.test import TestCase

from trader_rest.models import *
from .models import *

# Create your tests here.
user = UserProfile(gender='M', birthday='1953-02-10', email='email1@email.com', user_pw='user_pw1',name='name1', phone='phone1', description='description1')
user.save()
user = UserProfile(gender='M', birthday='1953-02-12', email='email2@email.com', user_pw='user_pw2',name='name2', phone='phone2', description='description2')
user.save()
user = UserProfile(gender='F', birthday='1953-02-13', email='email3@email.com', user_pw='user_pw3',name='name3', phone='phone3', description='description3')
user.save()

addr= UserAddress(uid= UserProfile.objects.get(pk=1),address1='address1', city='city1',nation='nation1',post='post1')
addr.save()
addr= UserAddress(uid= UserProfile.objects.get(pk=1),address1='address2', city='city2',nation='nation1',post='post2')
addr.save()
addr= UserAddress(uid= UserProfile.objects.get(pk=2),address1='address3', city='city1',nation='nation1',post='post3')
addr.save()
addr= UserAddress(uid= UserProfile.objects.get(pk=2),address1='address4', city='city1',nation='nation1',post='post4')
addr.save()
addr= UserAddress(uid= UserProfile.objects.get(pk=3),address1='address5', city='city2',nation='nation1',post='post5')
addr.save()

login= UserLogin(uid= UserProfile.objects.get(pk=1), device = 'Android4.3', ip='192.168.1.1')
login.save()

catalog = ProductCatalog(product_catalog_name='Books & Audible')
catalog.save()
catalog = ProductCatalog(product_catalog_name='Movies, Music & Games')
catalog.save()
catalog = ProductCatalog(product_catalog_name='Electronics & Computers')
catalog.save()
catalog = ProductCatalog(product_catalog_name='Home, Garden & Tools')
catalog.save()
catalog = ProductCatalog(product_catalog_name='Beauty, Health & Grocery')
catalog.save()
catalog = ProductCatalog(product_catalog_name='Toy, Kids & Baby')
catalog.save()
catalog = ProductCatalog(product_catalog_name='Sports & Outdoors')
catalog.save()
catalog = ProductCatalog(product_catalog_name='Clothing, Shoes & Jewelry')
catalog.save()
catalog = ProductCatalog(product_catalog_name='Automotive & Industrial')
catalog.save()

item = ProductCatalogItem(item_name='Brand', item_required='true', product_catalog=ProductCatalog.objects.get(product_catalog_name='Clothing, Shoes & Jewelry'))
item.save()
item = ProductCatalogItem(item_name='Product Number', item_required='true', product_catalog=ProductCatalog.objects.get(product_catalog_name='Clothing, Shoes & Jewelry'))
item.save()

#order = UserOrder(expect_date='2014-03-12', description='order description', expect_price='$123.11', order_status='A', uid= UserProfile.objects.get(pk=1), product_catalog=ProductCatalog.objects.get(product_catalog_name='Clothing, Shoes & Jewelry'), order_address=UserAddress.objects.get(pk=1))
order = UserOrder(expect_date='2014-03-12', description='order description', order_time='2014-04-09',expect_price='$123.11', uid= UserProfile.objects.get(pk=1), product_catalog=ProductCatalog.objects.get(product_catalog_name='Clothing, Shoes & Jewelry'), order_address=UserAddress.objects.get(pk=1))
order.save()
#order = UserOrder(expect_date='2014-03-12', description='order description', expect_price='$123.11', order_status='A', uid= UserProfile.objects.get(pk=1), product_catalog=ProductCatalog.objects.get(product_catalog_name='Clothing, Shoes & Jewelry'), order_address=UserAddress.objects.get(pk=1))
orderExtraInfo = UserOrderExtraInfo(order=UserOrder.objects.get(pk=1), item=ProductCatalogItem.objects.get(item_name='Brand'),item_value = 'Tiffany')
orderExtraInfo.save()
orderExtraInfo = UserOrderExtraInfo(order=UserOrder.objects.get(pk=1), item=ProductCatalogItem.objects.get(item_name='Product Number'),item_value = 'No.001')
orderExtraInfo.save()