from rest_framework import serializers
from .models import Wallet
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    user_email = serializers.SlugRelatedField(slug_field='email', read_only=True, source='user')  # Display user's email
    user_name = serializers.SlugRelatedField(slug_field='full_name', read_only=True, source='user')  # Display user's full name

    class Meta:
        model = Transaction
        fields = ['transaction_id', 'reference_number', 'user_email', 'user_name', 'status']



class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user', 'balance']
