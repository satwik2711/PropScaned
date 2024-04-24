from rest_framework import serializers
from .models import *
from property_listing.serializers import PropertyType1Serializer, PropertyType2Serializer, PropertyType3Serializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropScanUser
        fields = ['full_name', 'phone_no', 'email', 'user_type', 'password', 'favorites_type1', 'favorites_type2', 'favorites_type3']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'phone_no': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)  # Remove password from validated_data
        user = PropScanUser.objects.create_user(**validated_data)
        if password:
            user.set_password(password)  # Set password if provided
            user.save()
        return user
    
class BuyerSerializer(serializers.Serializer):
    user = UserSerializer()
    class Meta:
        model = Buyer
        fields = ['id', 'user', 'main_image_link']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            new_user = user_serializer.save()
            buyer, created = Buyer.objects.update_or_create(user=new_user, **validated_data)
            return buyer


class BrokerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Broker
        fields = ['id', 'user', 'rera_registered', 'license_type', 'company_name', 'company_url', 'company_address_1', 'company_address_2', 'city', 'description', 'main_image_link', 'additional_phone_no_1', 'additional_phone_no_2', 'landline_number_1', 'landline_number_2']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            new_user = user_serializer.save()
            broker, created = Broker.objects.update_or_create(user=new_user, **validated_data)
            return broker
    
class OwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Owner
        fields = ['id', 'user', 'additional_phone_no', 'main_image_link']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            new_user = user_serializer.save()
            owner, created = Owner.objects.update_or_create(user=new_user, **validated_data)
            return owner
