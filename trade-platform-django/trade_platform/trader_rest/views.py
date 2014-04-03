from rest_framework import generics
from rest_framework.response import Response

from .models import *
from .serializers import *


class UserList(generics.ListCreateAPIView):
    queryset  = UserProfile.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user profile instance.
    """
    queryset  = UserProfile.objects.all()
    serializer_class = UserSerializer
    
class AddressList(generics.ListCreateAPIView):
    queryset  = UserAddress.objects.all()
    serializer_class = AddressSerializer

class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user address instance.
    """
    queryset  = UserAddress.objects.all()
    serializer_class = UserSerializer