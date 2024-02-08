from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Inbound_Product)
admin.site.register(Outbound_Product)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(UserProfile)

