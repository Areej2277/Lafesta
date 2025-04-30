from django.contrib import admin
from .models import Shipment ,Payment


# Register your models here.
class ShipmentAdmin(admin.ModelAdmin):
    list_display=('')
admin.site.register(Shipment)
admin.site.register(Payment)


