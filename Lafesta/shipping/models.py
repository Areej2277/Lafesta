from django.db import models
from dresses.models import Rental

# Create your models here.
class Shipment(models.Model):
    request= models.ForeignKey(Rental, on_delete=models.CASCADE)
    shipping_company=models.CharField(max_length=100)
    pickup_information=models.TextField()
    Expected_delivery_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Statuschoices(models.TextChoices):
        status1='Shipment Created','Shipment Created'
        status2='Picked Up from Sender','Picked Up from Sender'
        status3='In Transit','In Transit'
        status4='out for Delivery','out for Delivery'
        status5='Delivered','Delivered'
        status6='Delivery Failed','Delivery Failed'
        status7='On Hold','On Hold'
        status8='Returned to Sender','Returned to Sender'
        status9='Shipment Canceled','Shipment Canceled'
        
    status=models.CharField(choices=Statuschoices.choices)