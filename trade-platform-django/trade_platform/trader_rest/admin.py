from django.contrib import admin

from .models import OrderImage
from .models import OrderTopics
from .models import ProductCatalog
from .models import ProductCatalogItem
from .models import TopicComments
from .models import UserAddress
from .models import UserLogin
from .models import UserOrder
from .models import UserOrderExtraInfo
from .models import UserProfile
from .models import UserrQuote


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserAddress)
admin.site.register(UserLogin)
admin.site.register(ProductCatalog)
admin.site.register(ProductCatalogItem)
admin.site.register(UserOrder)
admin.site.register(OrderImage)
admin.site.register(UserOrderExtraInfo)
admin.site.register(OrderTopics)
admin.site.register(TopicComments)
admin.site.register(UserrQuote)
