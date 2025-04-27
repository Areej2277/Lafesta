from django.db import models
from django.contrib.auth.models import User
#from اسم الاب حق الفساتين import اسم المودل حق الفساتين 
#سوي امبورت لكلاس الفساتين 

# Create your models here.

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #الدريس هنا هو اسم الموديل حق الفساتين اللي تسويه ايمان 
    #dress = models.ForeignKey(Dress, on_delete=models.CASCADE)

    created_at=models.DateTimeField(auto_now_add=True)

class Rentalrequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #dress = models.ForeignKey(dress, on_delete=models.CASCADE)
    rentalDuration=models.IntegerField(choices=[(1,1),(2,2),(3,3)])
    created_at=models.DateTimeField(auto_now_add=True)
    request_status=models.CharField(max_length=100, choices=[
        ('Confirmed','Confirmed'),
        ('Not Confirmed','Not Confirmed')
    ])

class Adress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city=models.CharField(max_length=100)
    neighborhood=models.CharField(max_length=100)
    postcode=models.IntegerField()
    comments=models.TextField()


# class  Payment (models.Model):
#     request= models.ForeignKey(Rentalrequest, on_delete=models.CASCADE)
#     created_at=models.DateTimeField(auto_now_add=True)
#     refID=models.IntegerField()
#     status=models.CharField(max_length=100 ,choices=[
#         ('Paid','Paid'),
#         ('Processing','Processing'),
#         ('Failed','Failed'),
#         ('Refunded','Refunded')
#     ])


