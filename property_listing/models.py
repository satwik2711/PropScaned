from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import datetime

from accounts.models import PropScanUser


class PropertyType1(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('flat', 'Flat'),
        ('villa', 'Villa'),
        ('builder_floor', 'Builder Floor')
    ]

    FURNISHING_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]

    OWNERSHIP_CHOICES = [
        ('freehold', 'Freehold'),
        ('leasehold', 'Leasehold'),
        ('co_op', 'Co-Op'),
        ('power_of_attorney', 'Power of Attorney'),
    ]

    PROPERTY_AVAILABILITY_CHOICES = [
        ('ready_to_move', 'Ready to Move'),
        ('under_construction', 'Under Construction'),
    ]

    PRICE_CHOICES = [
        ('all_inclusive_price', 'All Inclusive Price'),
        ('tax_govt_charges_excluded', 'Tax and Govt Charges Excluded'),
        ('price_negotiable', 'Price Negotiable'),
    ]

    LISTING_TYPE_CHOICES = [ #
        ('rent','Rent'), 
        ('sell','Sell'),
        ('pg','PG'),
    ]

    PROPERTY_SUB_TYPE_CHOICES = [
        ('resedential','Resedential'),
        ('commercial','Commercial')
    ]
    
    BROKERAGE_TYPE_CHOICES =[
        ('fixed','Fixed'),
        ('percentage_of_price','Percentage of price')
    ]

    CRM_STATUS_CHOICES = [
        ('Listed', 'Listed'),
        ('Enquiry received', 'Enquiry received'),
        ('Qualified', 'Qualified'),
        ('Call scheduled', 'Call scheduled'),
        ('On-site meeting scheduled', 'On-site meeting scheduled'),
        ('Quotation sent', 'Quotation sent'),
        ('Negotiation', 'Negotiation'),
        ('Sold', 'Sold'),
        ('Archived', 'Archived'),
        ('Unlisted', 'Unlisted')    
    ]

    user = models.ForeignKey(PropScanUser, on_delete=models.CASCADE)
    is_listed = models.BooleanField(default=True)
    propscan_id = models.CharField(max_length=250, null=True) # ML ID
    #crm
    status = models.CharField(max_length=100, default="Listed", choices=CRM_STATUS_CHOICES)
    contacted = models.BooleanField(default=False)
    #crm 
    #selling property
    sold_date = models.DateField(null=True, blank=True)
    final_selling_price = models.PositiveIntegerField(null=True, blank=True)
    #selling property
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES)
    property_sub_type = models.CharField(max_length=20, choices=PROPERTY_SUB_TYPE_CHOICES) #
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES) #
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    locality_society = models.CharField(max_length=100)
    sub_locality = models.CharField(max_length=100)
    flat_number = models.CharField(max_length=20, null=True, blank=True)
    house_number = models.CharField(max_length=20, null=True, blank=True)
    floor_number = models.CharField(max_length=20, null=True, blank=True)
    bhk_type = models.CharField(max_length=10)
    super_built_up_area = models.DecimalField(max_digits=10, decimal_places=2)
    built_up_area = models.DecimalField(max_digits=10, decimal_places=2)
    carpet_area = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
    balconies = models.PositiveSmallIntegerField()
    other_rooms = models.CharField(max_length=100)
    furnishing_type = models.CharField(max_length=20, choices=FURNISHING_CHOICES)
    parking_available = models.BooleanField()
    covered_parking = models.BooleanField()
    total_floors = models.PositiveSmallIntegerField()
    availability_status = models.CharField(max_length=20, choices=PROPERTY_AVAILABILITY_CHOICES)
    age_of_property = models.PositiveSmallIntegerField()
    #images
    main_image_link = models.URLField(max_length=200, blank=True, null=True)
    additional_images_link = models.TextField(max_length=200, blank=True, null=True)
    #images
    #time fields
    created_time = models.DateTimeField(default=timezone.now, editable=False)
    updated_time = models.DateTimeField(auto_now=True)
    #time fields    
    ownership_type = models.CharField(max_length=20, choices=OWNERSHIP_CHOICES)
    expected_price = models.PositiveIntegerField()
    price_per_sq_ft = models.DecimalField(max_digits=10, decimal_places=2)
    price_type = models.CharField(max_length=30, choices=PRICE_CHOICES)
    maintenance_amount = models.PositiveIntegerField()
    expected_rental = models.PositiveIntegerField()
    booking_amount = models.PositiveIntegerField()
    annual_dues_payable = models.PositiveIntegerField()
    membership_charge = models.PositiveIntegerField()
    unique_description = models.TextField()
    brokerage = models.BooleanField()
    brokerage_type = models.CharField(max_length=20, choices=BROKERAGE_TYPE_CHOICES, null=True)
    brokerage_amount = models.PositiveIntegerField(null=True)
    negotiable = models.BooleanField(null=True)
    maintenance_staff = models.BooleanField()
    water_storage = models.BooleanField()
    rain_water_harvesting = models.BooleanField()
    vaastu_compliant = models.BooleanField()
    solar_panels = models.BooleanField()
    overlooking_pool = models.BooleanField()
    overlooking_park = models.BooleanField()
    overlooking_club = models.BooleanField()
    overlooking_main_road = models.BooleanField()
    gated_society = models.BooleanField()
    corner_property = models.BooleanField()
    property_facing_direction = models.CharField(max_length=20)
    location_advantages = models.TextField()

    def __str__(self):
        return f"{self.property_type} in {self.locality_society} - {self.expected_price}"
    
    class Meta:
        verbose_name = 'propertytype1'

class PropertyType2(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('studio_apt', 'Studio Apartment'),
        ('serviced', 'Serviced Apartment'),
        ('farmhouse', 'Farmhouse')
    ]
    FURNISHING_CHOICES = [
        ('unfurnished', 'Unfurnished'),
        ('semi_furnished', 'Semi Furnished'),
        ('fully_furnished', 'Fully Furnished')
    ]
    OWNERSHIP_CHOICES = [
        ('freehold', 'Freehold'),
        ('leasehold', 'Leasehold'),
        ('co_op', 'Co-operative Society'),
        ('power_of_attorney', 'Power of Attorney')
    ]

    LISTING_TYPE_CHOICES = [
        ('rent','Rent'),
        ('sell','Sell'),
        ('pg','PG'),
    ]

    PROPERTY_SUB_TYPE_CHOICES = [
        ('resedential','Resedential'),
        ('commercial','Commercial')
    ]

    PROPERTY_AVAILABILITY_CHOICES = [
        ('ready_to_move', 'Ready to Move'),
        ('under_construction', 'Under Construction'),
    ]

    BROKERAGE_TYPE_CHOICES =[
        ('fixed','Fixed'),
        ('percentage_of_price','Percentage of price')
    ]

    CRM_STATUS_CHOICES = [
        ('Listed', 'Listed'),
        ('Enquiry received', 'Enquiry received'),
        ('Qualified', 'Qualified'),
        ('Call scheduled', 'Call scheduled'),
        ('On-site meeting scheduled', 'On-site meeting scheduled'),
        ('Quotation sent', 'Quotation sent'),
        ('Negotiation', 'Negotiation'),
        ('Sold', 'Sold'),
        ('Archived', 'Archived'),
        ('Unlisted', 'Unlisted')
    ]
    user = models.ForeignKey(PropScanUser, on_delete=models.CASCADE)
    is_listed = models.BooleanField(default=True)
    propscan_id = models.CharField(max_length=250, null=True) # ML ID
    #crm
    status = models.CharField(max_length=100, default="Listed", choices=CRM_STATUS_CHOICES)
    contacted = models.BooleanField(default=False)
    #crm 
    #selling property
    sold_date = models.DateField(null=True, blank=True)
    final_selling_price = models.PositiveIntegerField(null=True, blank=True)
    #selling property
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    property_sub_type = models.CharField(max_length=20, choices=PROPERTY_SUB_TYPE_CHOICES)
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    locality_society = models.CharField(max_length=100)
    sub_locality = models.CharField(max_length=100)
    flat_number = models.CharField(max_length=50)
    bhk_type = models.CharField(max_length=10, null=True)
    super_built_up_area = models.DecimalField(max_digits=10, decimal_places=2)
    built_up_area = models.DecimalField(max_digits=10, decimal_places=2)
    carpet_area = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
    balconies = models.PositiveSmallIntegerField()
    other_rooms = models.CharField(max_length=100)
    furnishing = models.CharField(max_length=20, choices=FURNISHING_CHOICES)
    parking = models.BooleanField()
    covered_parking = models.BooleanField()
    total_floors = models.PositiveSmallIntegerField()
    floor_number = models.PositiveSmallIntegerField()
    availability_status = models.CharField(max_length=20,choices=PROPERTY_AVAILABILITY_CHOICES)
    age_of_property = models.PositiveSmallIntegerField()
    #images
    main_image_link = models.URLField(max_length=200, blank=True, null=True)
    additional_images_link = models.TextField(max_length=200, blank=True, null=True)
    #images
    #time fields
    created_time = models.DateTimeField(default=timezone.now, editable=False)
    updated_time = models.DateTimeField(auto_now=True)
    #time fields
    ownership = models.CharField(max_length=20, choices=OWNERSHIP_CHOICES)
    expected_price = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_sq_ft = models.DecimalField(max_digits=10, decimal_places=2)
    all_inclusive_price = models.BooleanField()
    tax_and_govt_charges_excluded = models.BooleanField()
    price_negotiable = models.BooleanField()
    maintenance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expected_rental = models.DecimalField(max_digits=10, decimal_places=2)
    booking_amount = models.DecimalField(max_digits=10, decimal_places=2)
    annual_dues_payable = models.DecimalField(max_digits=10, decimal_places=2)
    membership_charge = models.DecimalField(max_digits=10, decimal_places=2)
    unique_description = models.TextField()
    brokerage = models.BooleanField()
    brokerage_type = models.CharField(max_length=20, choices=BROKERAGE_TYPE_CHOICES, null=True)
    brokerage_amount = models.PositiveIntegerField(null=True)
    negotiable = models.BooleanField(null=True)
    maintenance_staff = models.BooleanField()
    water_storage = models.BooleanField()
    rain_water_harvesting = models.BooleanField()
    vaastu_compliant = models.BooleanField()
    solar_panels = models.BooleanField()
    overlooking_pool = models.BooleanField()
    overlooking_park = models.BooleanField()
    overlooking_club = models.BooleanField()
    overlooking_main_road = models.BooleanField()
    gated_society = models.BooleanField()
    corner_property = models.BooleanField()
    property_facing_direction = models.CharField(max_length=20)
    location_advantages = models.TextField()

    def __str__(self):
        return f"{self.property_type} in {self.locality_society} - {self.expected_price}"
    class Meta:
        verbose_name = 'propertytype2'


class PropertyType3(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('plot', 'Plot'),
    ]
    OWNERSHIP_CHOICES = [
        ('leasehold', 'Leasehold'),
        ('co-op_society', 'Co-op Society'),
        ('power_of_attorney', 'Power of Attorney'),
    ]
    LISTING_TYPE_CHOICES = [
        ('rent','Rent'),
        ('sell','Sell'),
        ('pg','PG'),
    ]
    PROPERTY_SUB_TYPE_CHOICES = [
        ('resedential','Resedential'),
        ('commercial','Commercial')
    ]
    PROPERTY_APPROVING_AUTHORITY_CHOICES = [
        ('rcuda', 'RCUDA'),
        ('cidc', 'CIDC'),
        ('nmmc', 'NMMC'),
    ]
    BROKERAGE_TYPE_CHOICES =[
        ('fixed','Fixed'),
        ('percentage_of_price','Percentage of price')
    ]
    CRM_STATUS_CHOICES = [
        ('Listed', 'Listed'),
        ('Enquiry received', 'Enquiry received'),
        ('Qualified', 'Qualified'),
        ('Call scheduled', 'Call scheduled'),
        ('On-site meeting scheduled', 'On-site meeting scheduled'),
        ('Quotation sent', 'Quotation sent'),
        ('Negotiation', 'Negotiation'),
        ('Sold', 'Sold'),
        ('Archived', 'Archived'),
        ('Unlisted', 'Unlisted')
    ]

    user = models.ForeignKey(PropScanUser, on_delete=models.CASCADE)
    is_listed = models.BooleanField(default=True)
    propscan_id = models.CharField(max_length=250, null=True) # ML ID
    #crm
    status = models.CharField(max_length=100, default="Listed", choices=CRM_STATUS_CHOICES)
    contacted = models.BooleanField(default=False)
    #crm 
    #selling property
    sold_date = models.DateField(null=True, blank=True)
    final_selling_price = models.PositiveIntegerField(null=True, blank=True)
    #selling property
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    property_sub_type = models.CharField(max_length=20, choices=PROPERTY_SUB_TYPE_CHOICES)
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    locality_society = models.CharField(max_length=100)
    sub_locality = models.CharField(max_length=100)
    plot_number = models.CharField(max_length=50)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    breadth = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    boundary_wall = models.BooleanField()
    number_of_open_sides = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    any_construction_done = models.BooleanField()
    no_of_sheds_constructed = models.PositiveIntegerField(null=True)
    no_of_rooms_constructed = models.PositiveIntegerField(null=True)
    no_of_washrooms_constructed = models.PositiveIntegerField(null=True)
    number_of_floors_allowed_for_construction = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    possession_expected_date = models.DateField()
    #images
    main_image_link = models.URLField(max_length=200, blank=True, null=True)
    additional_images_link = models.TextField(max_length=200, blank=True, null=True)
    #images
    #time fields
    created_time = models.DateTimeField(default=timezone.now, editable=False)
    updated_time = models.DateTimeField(auto_now=True)
    #time fields
    ownership = models.CharField(max_length=20, choices=OWNERSHIP_CHOICES)
    property_approving_authority = models.CharField(max_length=10, choices=PROPERTY_APPROVING_AUTHORITY_CHOICES)
    expected_price = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_sq_ft = models.DecimalField(max_digits=10, decimal_places=2)
    all_inclusive_price = models.BooleanField()
    tax_and_govt_charges_excluded = models.BooleanField()
    price_negotiable = models.BooleanField()
    maintenance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expected_rental = models.DecimalField(max_digits=10, decimal_places=2)
    booking_amount = models.DecimalField(max_digits=10, decimal_places=2)
    annual_dues_payable = models.DecimalField(max_digits=10, decimal_places=2)
    membership_charge = models.DecimalField(max_digits=10, decimal_places=2)
    unique_description = models.TextField()
    brokerage = models.BooleanField()
    brokerage_type = models.CharField(max_length=20, choices=BROKERAGE_TYPE_CHOICES, null=True)
    brokerage_amount = models.PositiveIntegerField(null=True)
    negotiable = models.BooleanField(null=True)
    maintenance_staff = models.BooleanField()
    water_storage = models.BooleanField()
    rain_water_harvesting = models.BooleanField()
    vaastu_compliant = models.BooleanField()
    solar_panels = models.BooleanField()
    overlooking_pool = models.BooleanField()
    overlooking_park = models.BooleanField()
    overlooking_club = models.BooleanField()
    overlooking_main_road = models.BooleanField()
    gated_society = models.BooleanField()
    corner_property = models.BooleanField()
    property_facing_direction = models.CharField(max_length=20)
    location_advantages = models.TextField()

    def __str__(self):
        return f"{self.property_type} in {self.locality_society} - {self.expected_price}"
    
    class Meta:
        verbose_name = 'propertytype3'
    

class Counter(models.Model):
    id = models.IntegerField(primary_key=True)
    meet_calls = models.PositiveIntegerField(default=0)
    chat_calls = models.PositiveIntegerField(default=0)
    property_calls = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"ID: {self.id}"