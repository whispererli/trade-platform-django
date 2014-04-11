from django.conf.urls import patterns, url
from rest_framework.authtoken import views as rest_view
from rest_framework.urlpatterns import format_suffix_patterns

import views


urlpatterns = patterns('trader_rest.views',
    url(r'^user/$', views.UserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^userProfile/$', views.UserProfileList.as_view()),
    url(r'^userProfile/(?P<pk>[0-9]+)/$', views.UserProfileDetail.as_view()),
    url(r'^address/$', views.AddressList.as_view()),
    url(r'^address/(?P<pk>[0-9]+)/$', views.AddressDetail.as_view()),
    url(r'^catalog/$', views.ProductCatalogList.as_view()),
    url(r'^catalog/(?P<pk>[0-9]+)/$', views.ProductCatalogDetail.as_view()), 
    url(r'^catalogItem/$', views.ProductCatalogItemList.as_view()),
    url(r'^catalogItem/(?P<pk>[0-9]+)/$', views.ProductCatalogItemDetail.as_view()), 
    url(r'^userOrder/$', views.UserOrderListByFilter.as_view()),
    url(r'^makeOrder/$', views.make_order),
    url(r'^make_comment/$', views.make_comment),
    url(r'^api-token-auth/', rest_view.obtain_auth_token)
)
                            
urlpatterns = format_suffix_patterns(urlpatterns)