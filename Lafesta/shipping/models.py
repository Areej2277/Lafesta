from django.db import models
from customer.models import Rentalrequest

# Create your models here.
class Shipment(models.Model):
    request= models.ForeignKey(Rentalrequest, on_delete=models.CASCADE)
    shipping_company=models.CharField(max_length=100)
    pickup_information=models.TextField()
    Expected_delivery_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=100 ,choices=[
        ('Shipment Created','Shipment Created'),
        ('Picked Up from Sender','Picked Up from Sender'),
        ('In Transit','In Transit'),
        ('out for Delivery','out for Delivery'),
        ('Delivered','Delivered'),
        ('Delivery Failed','Delivery Failed'),
        ('On Hold','Delivery Failed'),
        ('Returned to Sender','Returned to Sender'),
        ('Shipment Canceled','Shipment Canceled')
    ])