from django.db import models
from dresses.models import Rental
from customer.models import Adress


# Create your models here.
class Shipment(models.Model):
    adress=models.ForeignKey(Adress, on_delete=models.CASCADE)
    #rental= models.ForeignKey(Rental, on_delete=models.CASCADE)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='shipment')  # ✅ التعديل هنا

    shipping_company=models.CharField(max_length=100)
    pickup_information=models.TextField()
    expected_delivery_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Statuschoices(models.TextChoices):
        status1='Shipment Created','Shipment Created'
        status2='Picked Up from Sender','Picked Up from Sender'
        status3='In Transit','In Transit'
        status4='Out for Delivery','Out for Delivery'
        status5='Delivered','Delivered'
        status6='Delivery Failed','Delivery Failed'
        status7='On Hold','On Hold'
        status8='Returned to Sender','Returned to Sender'
        status9='Shipment Canceled','Shipment Canceled'
        
    status=models.CharField(choices=Statuschoices.choices ,max_length=100 ,default="Shipment Created")

    def __str__(self) -> str:
        return self.shipping_company

class  Payment (models.Model):
   # request= models.ForeignKey(Rental, on_delete=models.CASCADE)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='payment')#هذا التعديل يسمح لنا نستدعي payment من اي مكان 

    created_at=models.DateTimeField(auto_now_add=True)
    refID=models.IntegerField()
    #بعد ما يتم الربط بالمنصات لا تنسي تحذفي معلومات البطاقة حقت اليوزر
    card_number=models.IntegerField()
    card_holder_name=models.CharField(max_length=100)
    expiry_date=models.DateField()
    cvv=models.IntegerField()
    class StatusChoices(models.TextChoices):
        Status1='Paid','Paid'
        Status2='Processing','Processing'
        Status3='Refunded','Refunded'
    status=models.CharField(choices=StatusChoices.choices ,max_length=100)
    def __int__(self)->int:
        return self.refID
