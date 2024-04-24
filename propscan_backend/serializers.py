# from django.http import JsonResponse
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework import serializers

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         # Customize the payload data as per your requirements
#         token = super().get_token(user)
#         token['email'] = user.email
#         token['phone'] = user.phone_number
#         return token

#     def validate(self, attrs):
#         data = super().validate(attrs)
#         refresh = self.get_token(self.user)

#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)

#         return data
from rest_framework import serializers

class TokenObtainSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    email = serializers.EmailField()
