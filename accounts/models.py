from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class PropScanUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class PropScanUser(AbstractUser):
    BUYER = 'BUYER'
    OWNER = 'OWNER'
    BROKER = 'BROKER'

    USER_TYPE_CHOICES = [
        (BUYER, "BUYER"),
        (OWNER, "OWNER"),
        (BROKER, "BROKER")
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=BUYER, null=False)
    full_name = models.CharField(max_length=256, null=True)
    phone_no = models.CharField(
        max_length=14, 
        null=False, 
        blank=False, 
        validators=[
            RegexValidator(
                r'^\+91\d{10}$', 
                message="Phone number must be entered in the format: '+919876543210'. '+91' followed by 10 digits",
                code='invalid_phonenumber'
            )
        ]
    )
    favorites_type1 = models.ManyToManyField('property_listing.PropertyType1', related_name='favorited_by', blank=True)
    favorites_type2 = models.ManyToManyField('property_listing.PropertyType2', related_name='favorited_by', blank=True)
    favorites_type3 = models.ManyToManyField('property_listing.PropertyType3', related_name='favorited_by', blank=True)
    objects = PropScanUserManager()
    
    def __str__(self):
        return self.email


class Buyer(models.Model):
    user = models.OneToOneField(PropScanUser, on_delete=models.CASCADE, null = True)
    main_image_link = models.URLField(blank=True, null=True)

class Owner(models.Model):
    user = models.OneToOneField(PropScanUser, on_delete=models.CASCADE)
    additional_phone_no = models.CharField(
        max_length=14, 
        null=True, 
        blank=True, 
        validators=[
            RegexValidator(
                r'^\+91\d{10}$', 
                message="Phone number must be entered in the format: '+919876543210'. '+91' followed by 10 digits",
                code='invalid_phonenumber'
            )
        ]
    )
    main_image_link = models.URLField(blank=True, null=True)


class Broker(models.Model):
    user = models.OneToOneField(PropScanUser, on_delete=models.CASCADE)
    LICENSE_TYPE_CHOICES = [
        ("1", "Individual"),
        ("2", "Firm")
    ]
    RERA_REGISTERED_CHOICES = [
        ("Yes", "Yes"),
        ("Applied", "I have applied"),
        ("NotApplicable", "Not Applicable")
    ]

    rera_registered = models.CharField(max_length=20, choices=RERA_REGISTERED_CHOICES)
    license_type = models.CharField(max_length=20, choices=LICENSE_TYPE_CHOICES)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_url = models.URLField(max_length=200, blank=True, null=True)
    company_address_1 = models.CharField(max_length=256)
    company_address_2 = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=50)
    description = models.TextField()
    main_image_link = models.URLField(blank=True, null=True)
    additional_phone_no_1 = models.CharField(
        max_length=14, 
        null=True, 
        blank=True, 
        validators=[
            RegexValidator(
                r'^\+91\d{10}$', 
                message="Phone number must be entered in the format: '+919876543210'. '+91' followed by 10 digits",
                code='invalid_phonenumber'
            )
        ]
    )
    additional_phone_no_2 = models.CharField(
        max_length=14, 
        null=True, 
        blank=True, 
        validators=[
            RegexValidator(
                r'^\+91\d{10}$', 
                message="Phone number must be entered in the format: '+919876543210'. '+91' followed by 10 digits",
                code='invalid_phonenumber'
            )
        ]
    )
    landline_number_1 = models.CharField(max_length=30, blank=True, null=True)
    landline_number_2 = models.CharField(max_length=30, blank=True, null=True)

