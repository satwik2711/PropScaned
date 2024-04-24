from django.contrib import admin
from .models import PropScanUser,Buyer,Owner,Broker
from django.contrib.auth.admin import UserAdmin


admin.site.register(PropScanUser, UserAdmin)
admin.site.register(Buyer)
admin.site.register(Owner)
admin.site.register(Broker)

