from django.db import models
from django.contrib.auth.models import User
from dresses.models import Dress, Rental

#from اسم الاب حق الفساتين import اسم المودل حق الفساتين 
#سوي امبورت لكلاس الفساتين 

# Create your models here.

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}"

class Adress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rental=models.OneToOneField(Rental, on_delete=models.CASCADE)
    class Companychoices(models.TextChoices):
        company1="Aramex","Aramex"
        company2="SMSA Express","SMSA Express"
    shipping_company=models.CharField(choices=Companychoices.choices ,max_length=100 ,default="Aramex")
    class Citychoices(models.TextChoices):
        city1="riyadh","Riyadh"
        city2="jeddah","Jeddah"
        city3="dammam","Dammam"
        city4="abha","Abha"
    city=models.CharField(choices=Citychoices.choices ,max_length=100)
    neighborhood=models.CharField(max_length=100)
    postcode=models.IntegerField()
    comments=models.TextField()
    def __str__(self) -> str:
        return f"{self.user.username} - {self.city}, {self.neighborhood}, {self.postcode}"



# class  Payment (models.Model):
#     request= models.ForeignKey(Rentalrequest, on_delete=models.CASCADE)
#     created_at=models.DateTimeField(auto_now_add=True)
#     refID=models.IntegerField()
#       clss StatusChoices(models.TextChoices):
#           Status1='Paid','Paid'
#           Status2='Processing','Processing'
#           Status3='Refunded','Refunded'
#           
#     status=models.CharField(choices=StatusChoices.choices)


