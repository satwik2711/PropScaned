from django.db import models
from accounts.models import PropScanUser
import uuid

class Wallet(models.Model):
    user = models.OneToOneField(PropScanUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.phone_no}'s Wallet"
    
class Transaction(models.Model):
    user = models.ForeignKey(PropScanUser, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255)  # From Razorpay
    reference_number = models.CharField(max_length=255, default='PS' + uuid.uuid4().hex[:8])
    status = models.CharField(max_length=255)  # From Razorpay

    def __str__(self):
        return f"Transaction {self.reference_number} for user {self.user.email}"