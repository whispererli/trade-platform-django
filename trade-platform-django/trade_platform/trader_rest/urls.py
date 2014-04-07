from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

import views


urlpatterns = patterns('trader_rest.views',
    url(r'^user/$', views.UserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^address/$', views.AddressList.as_view()),
    url(r'^address/(?P<pk>[0-9]+)/$', views.AddressDetail.as_view()),
    url(r'^catalog/$', views.ProductCatalogList.as_view()),
    url(r'^catalog/(?P<pk>[0-9]+)/$', views.ProductCatalogDetail.as_view()), 
    url(r'^catalogItem/$', views.ProductCatalogItemList.as_view()),
    url(r'^catalogItem/(?P<pk>[0-9]+)/$', views.ProductCatalogItemDetail.as_view()), 
    url(r'^userOrder/$', views.UserOrderList.as_view()),
    url(r'^makeOrder/$', views.user_order_details)
)
                            
urlpatterns = format_suffix_patterns(urlpatterns)