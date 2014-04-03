'''
Created on Apr 1, 2014

@author: m68li
'''
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    address = serializers.RelatedField(many=True)
    class Meta:
        model = UserProfile
        fields = ('gender', 'birthday','email', 'phone', 'description', 'address')
        write_only_fields  = ('user_pw', )
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('uid', 'address1', 'address2','city', 'nation', 'post')
        write_only_fields  = ('uid',)