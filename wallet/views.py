from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Wallet
from .serializers import WalletSerializer
import razorpay
from accounts.models import PropScanUser
from decimal import Decimal
from .models import Transaction
from .serializers import TransactionSerializer


@api_view(['GET'])
def wallet_list(request):
    
    wallets = Wallet.objects.all()
    serializer = WalletSerializer(wallets, many=True)
    return Response(serializer.data)

from .models import Transaction

@api_view(['POST'])
def add_funds(request, pk):
    user = get_object_or_404(PropScanUser, pk=pk)
    wallet, created = Wallet.objects.get_or_create(user=user, defaults={'balance': Decimal('0.00')})

    try:
        amount = Decimal(request.data.get('amount', '0'))
    except (ValueError, TypeError):
        return Response({'status': 'failed', 'error': 'Invalid amount.'}, status=status.HTTP_400_BAD_REQUEST)

    wallet.balance += amount
    wallet.save()

    amount_in_paise = int(amount * 100)

    client = razorpay.Client(auth=('rzp_test_YXsMVUW9TDcIlS', 'NkS5Ovh49TYm0FvlPT4LX5UM'))

    try:
        payment = client.order.create(dict(amount=amount_in_paise, currency='INR', payment_capture=1))
        transaction = Transaction.objects.create(
            user=user,
            transaction_id=payment['id'],
            status=payment['status'],
        )
    except Exception as e:
        wallet.balance -= amount
        wallet.save()
        return Response({'status': 'failed', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'status': 'success', 'data': payment, 'transaction': transaction.reference_number}, status=status.HTTP_200_OK)


@api_view(['GET'])
def transactions(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)