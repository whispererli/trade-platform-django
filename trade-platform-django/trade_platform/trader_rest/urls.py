from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
import views
urlpatterns = patterns('trader_rest.views',
    url(r'^user/$', views.UserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
     url(r'^address/$', views.AddressList.as_view()),
    url(r'^address/(?P<pk>[0-9]+)/$', views.AddressDetail.as_view()),
     
)
urlpatterns = format_suffix_patterns(urlpatterns)