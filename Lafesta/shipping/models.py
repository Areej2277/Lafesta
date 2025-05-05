from django.db import models
from dresses.models import Rental
from customer.models import Adress
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Shipment(models.Model):
    adress=models.ForeignKey(Adress, on_delete=models.CASCADE)
    #rental= models.ForeignKey(Rental, on_delete=models.CASCADE)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='shipment')  # ✅ التعديل هنا
    shipping_company=models.CharField(max_length=100)
    #pickup information
    owner_name=models.CharField(max_length=100)
    owner_phone= models.IntegerField()
    Pick_up_address=models.TextField()
    expected_Pick_up_date=models.DateTimeField()
    expected_delivery_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)


    tracking_url = models.URLField(blank=True, null=True)  # ✅ الحقل الجديد


    comments=models.TextField(blank=True, null=True)
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
    moyasar_id = models.CharField(max_length=255, unique=True)
   # request= models.ForeignKey(Rental, on_delete=models.CASCADE)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='payment')#هذا التعديل يسمح لنا نستدعي payment من اي مكان 
    amount=models.DecimalField(max_digits=8, decimal_places=2)
    moyasar_id=models.CharField(max_length=100,blank=True, null=True)
    invoice_url=models.URLField(max_length=300,blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    refID=models.IntegerField()
    class StatusChoices(models.TextChoices):
        Status1='paid','Paid'
        Status2='pending','pending'
        Status3='failed','failed'
    status=models.CharField(choices=StatusChoices.choices ,max_length=100 ,default='pending')
    def __str__(self)->str:
        return f"Payment for {self.rental} -{ self.status}"