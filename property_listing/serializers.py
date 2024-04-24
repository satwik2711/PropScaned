from rest_framework import serializers

from accounts.models import PropScanUser, Broker, Buyer, Owner
from .models import PropertyType1, PropertyType2, PropertyType3

#type1 ser
class PropertyType1Serializer(serializers.ModelSerializer):
    main_image_link = serializers.URLField(required=False)
    additional_images_link = serializers.CharField(required=False)

    class Meta:
        model = PropertyType1
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        additional_images = rep.get('additional_images_link', '')
        rep['additional_images_link'] = additional_images.split(',') if additional_images else []
        return rep


class PropertyType1SmallCardSerializer(serializers.ModelSerializer):
    user_display_name = serializers.SerializerMethodField()

    class Meta: 
        model = PropertyType1
        fields = ('id', 'main_image_link', 'bedrooms', 'expected_price', 'locality_society','user_display_name', 'super_built_up_area')

    def get_user_display_name(self, obj):
        user_type = obj.user.user_type
        if user_type == PropScanUser.BROKER:
            try:
                company_name = Broker.objects.get(user=obj.user).company_name
                if company_name:
                    return company_name
            except Broker.DoesNotExist:
                pass
        return obj.user.full_name


class PropertyType1LargeCardSerializer(serializers.ModelSerializer):
    user_display_name = serializers.SerializerMethodField()
    rera_registered = serializers.SerializerMethodField()

    class Meta: 
        model = PropertyType1
        fields = ('id', 'main_image_link', 'bedrooms', 'expected_price', 'locality_society',
                  'user_display_name', 'super_built_up_area', 
                  'rera_registered', 'availability_status', 'price_per_sq_ft')

    def get_user_display_name(self, obj):
        user_type = obj.user.user_type
        if user_type == PropScanUser.BROKER:
            try:
                broker = Broker.objects.get(user=obj.user)
                if broker.company_name:
                    return broker.company_name
            except Broker.DoesNotExist:
                pass
        return obj.user.full_name

    def get_rera_registered(self, obj):
        if obj.user.user_type == PropScanUser.BROKER:
            try:
                return Broker.objects.get(user=obj.user).rera_registered
            except Broker.DoesNotExist:
                return None
        else:
            return None

        
#type2 ser
class PropertyType2Serializer(serializers.ModelSerializer):
    main_image_link = serializers.URLField(required=False)
    additional_images_link = serializers.CharField(required=False)

    class Meta:
        model = PropertyType2
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        additional_images = rep.get('additional_images_link', '')
        rep['additional_images_link'] = additional_images.split(',') if additional_images else []
        return rep


class PropertyType2SmallCardSerializer(serializers.ModelSerializer):
    user_display_name = serializers.SerializerMethodField()

    class Meta: 
        model = PropertyType2
        fields = ('id', 'main_image_link', 'bedrooms', 'expected_price', 'locality_society', 'user_display_name', 'super_built_up_area')

    def get_user_display_name(self, obj):
        user_type = obj.user.user_type
        if user_type == PropScanUser.BROKER:
            try:
                company_name = Broker.objects.get(user=obj.user).company_name
                if company_name:
                    return company_name
            except Broker.DoesNotExist:
                pass
        return obj.user.full_name

class PropertyType2LargeCardSerializer(serializers.ModelSerializer):
    user_display_name = serializers.SerializerMethodField()
    rera_registered = serializers.SerializerMethodField()

    class Meta: 
        model = PropertyType2
        fields = ('id', 'main_image_link', 'bedrooms', 'expected_price', 'locality_society',
                  'user_display_name', 'super_built_up_area', 
                  'rera_registered', 'availability_status', 'price_per_sq_ft')

    def get_user_display_name(self, obj):
        user_type = obj.user.user_type
        if user_type == PropScanUser.BROKER:
            try:
                broker = Broker.objects.get(user=obj.user)
                if broker.company_name:
                    return broker.company_name
            except Broker.DoesNotExist:
                pass
        return obj.user.full_name

    def get_rera_registered(self, obj):
        if obj.user.user_type == PropScanUser.BROKER:
            try:
                return Broker.objects.get(user=obj.user).rera_registered
            except Broker.DoesNotExist:
                return None
        else:
            return None

#TYPE3 SER
class PropertyType3Serializer(serializers.ModelSerializer):
    main_image_link = serializers.URLField(required=False)
    additional_images_link = serializers.CharField(required=False)

    class Meta:
        model = PropertyType3
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        additional_images = rep.get('additional_images_link', '')
        rep['additional_images_link'] = additional_images.split(',') if additional_images else []
        return rep


class PropertyType3SmallCardSerializer(serializers.ModelSerializer):
    user_display_name = serializers.SerializerMethodField()

    class Meta: 
        model = PropertyType3
        fields = ('id', 'main_image_link', 'no_of_rooms_constructed', 'expected_price', 'locality_society', 'user_display_name', 'plot_area')

    def get_user_display_name(self, obj):
        user_type = obj.user.user_type
        if user_type == PropScanUser.BROKER:
            try:
                company_name = Broker.objects.get(user=obj.user).company_name
                if company_name:
                    return company_name
            except Broker.DoesNotExist:
                pass
        return obj.user.full_name

class PropertyType3LargeCardSerializer(serializers.ModelSerializer):
    user_display_name = serializers.SerializerMethodField()
    rera_registered = serializers.SerializerMethodField()

    class Meta: 
        model = PropertyType3
        fields = ('id', 'main_image_link', 'no_of_rooms_constructed', 'expected_price', 'locality_society',
                  'user_display_name', 'plot_area', 
                  'rera_registered', 'possession_expected_date', 'price_per_sq_ft')

    def get_user_display_name(self, obj):
        user_type = obj.user.user_type
        if user_type == PropScanUser.BROKER:
            try:
                broker = Broker.objects.get(user=obj.user)
                if broker.company_name:
                    return broker.company_name
            except Broker.DoesNotExist:
                pass
        return obj.user.full_name

    def get_rera_registered(self, obj):
        if obj.user.user_type == PropScanUser.BROKER:
            try:
                return Broker.objects.get(user=obj.user).rera_registered
            except Broker.DoesNotExist:
                return None
        else:
            return None

#CRM SERIALIZER

class PropertyType1CRMSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType1
        fields = ('id', 'locality', 'city', 'expected_price', 'contacted')

class PropertyType2CRMSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType2
        fields = ('id', 'locality', 'city', 'expected_price', 'contacted')

class PropertyType3CRMSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType3
        fields = ('id', 'locality', 'city', 'expected_price', 'contacted')