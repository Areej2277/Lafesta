from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from .models import Shipment ,Payment
from dresses.models import Rental
from customer.models import Adress
import random


# Create your views here.
def create_payment(request:HttpRequest,request_id):
    rental_request =Rental.objects.get(pk=request_id)

    if request.method=="POST":
        new_payment=Payment(card_number=request.POST["card_number"], card_holder_name=request.POST["card_holder_name"],expiry_date=request.POST["expiry_date"],cvv=request.POST["cvv"],refID=random.randint(100000, 999999), tatus='Paid',request=rental_request)
        new_payment.save()
        # لو فيه حقل rental: rental=rental_request
        return redirect('shipping:Payment_confirmation', payment_id=new_payment.id, rental_request_id=rental_request.id)
        
    return render(request ,'shipping/new_payment.html' ,{'rental': rental_request})


def create_shipment(request:HttpRequest ,request_id):
    rental_request=Rental.objects.get(pk=request_id)
    adress = Adress.objects.filter(user=rental_request.customer).first()

    if request.method=="POST":
        new_Shipment=Shipment(shipping_company=request.POST["shipping_company"], pickup_information=request.POST["pickup_information"],expected_delivery_date=request.POST["expected_delivery_date"],request=rental_request,adress=adress)
        new_Shipment.save()
        
        return redirect('dresses:rental_requests')
        
        
    return render(request ,'shipping/new_shipment.html',{'rental': rental_request})

def Payment_confirmation(request:HttpRequest, payment_id ,rental_request_id):
    
    payment = Payment.objects.get(id=payment_id)
    rental_request= Rental.objects.get(id=rental_request_id)

    return render(request ,'shipping/Payment_confirmation.html',{'payment':payment},{'rental': rental_request})
