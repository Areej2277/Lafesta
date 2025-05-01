from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from .models import Shipment ,Payment
from dresses.models import Rental
from customer.models import Adress
from django.contrib import messages
from datetime import datetime
import random
from django.contrib.auth.decorators import login_required



# Create your views here.
def create_payment(request:HttpRequest,  rental_id):
    rental =Rental.objects.get(pk= rental_id)

    if request.method=="POST":
        expiry_input = request.POST["expiry_date"]  # مثل: "2026-02"
        expiry_full = expiry_input + "-01"  # نضيف اليوم الأول لتكوين تاريخ صحيح
        expiry_date = datetime.strptime(expiry_full, "%Y-%m-%d").date()
        new_payment=Payment(card_number=request.POST["card_number"], card_holder_name=request.POST["card_holder_name"],expiry_date=expiry_date,cvv=request.POST["cvv"],refID=random.randint(100000, 999999), status='Paid',rental=rental)
        new_payment.save()
        # ✅ تحديث حالة الطلب إلى confirmed
        rental.status = 'confirmed'
        rental.save()


        messages.success(request, "Payment was created successfully!")
        # لو فيه حقل rental: rental=rental_request
        return redirect('shipping:Payment_confirmation', payment_id=new_payment.id, rental_id=rental.id)
    else:
        messages.error(request, "Payment creation failed")
        
    return render(request ,'shipping/new_payment.html' ,{'rental': rental})


# def create_shipment(request:HttpRequest ,request_id):
#     rental_request=Rental.objects.get(pk=request_id)
#     adress = Adress.objects.filter(user=rental_request.customer).first()

#     if request.method=="POST":
#         new_Shipment=Shipment(shipping_company=request.POST["shipping_company"], pickup_information=request.POST["pickup_information"],expected_delivery_date=request.POST["expected_delivery_date"],request=rental_request,adress=adress)
#         new_Shipment.save()
        
#         return redirect('dresses:rental_requests')
        
        
#     return render(request ,'shipping/new_shipment.html',{'rental': rental_request})

@login_required
def create_shipment(request:HttpRequest ,request_id):
    rental_request = Rental.objects.get(pk=request_id)

    # ✅ تأكد أن المستخدم هو مالك الفستان
    if request.user != rental_request.dress.owner:
        from django.contrib import messages
        messages.error(request, "You are not authorized to create a shipment for this dress.")
        return redirect('main:home')

    # ✅ جلب عنوان الكاستمر
    adress = Adress.objects.filter(user=rental_request.customer).first()

    if request.method == "POST":
        new_Shipment = Shipment(
            shipping_company=request.POST["shipping_company"],
            pickup_information=request.POST["pickup_information"],
            expected_delivery_date=request.POST["expected_delivery_date"],
            request=rental_request,
            adress=adress
        )
        new_Shipment.save()

        # ✅ بعد الإنشاء يروح لصفحة إدارة الشحنات
        return redirect('shipping:manage_shipments')

    return render(request, 'shipping/new_shipment.html', {'rental': rental_request})




def Payment_confirmation(request:HttpRequest, payment_id ,rental_id):
    
    payment = Payment.objects.get(id=payment_id)
    rental= Rental.objects.get(id=rental_id)

    return render(request ,'shipping/Payment_confirmation.html',{'payment':payment ,'rental': rental})


def track_shipment(request: HttpRequest, rental_id):
    rental = Rental.objects.get(id=rental_id, customer=request.user)

    shipment = Shipment.objects.filter(rental=rental).first()

    return render(request, 'shipping/track_shipment.html', {
        'rental': rental,
        'shipment': shipment
    })



@login_required
def manage_shipments(request):
    user = request.user

    # جلب جميع الشحنات المرتبطة بفستاتين المالك
    shipments = Shipment.objects.filter(request__dress__owner=user).order_by('-created_at')

    return render(request, 'shipping/manage_shipments.html', {'shipments': shipments})


@login_required
def update_shipment_status(request, shipment_id):
    shipment = Shipment.objects.get(id=shipment_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        shipment.status = new_status
        shipment.save()
        messages.success(request, "Shipment status updated successfully.")
        return redirect('shipping:manage_shipments')

    return render(request, 'shipping/update_shipment_status.html', {'shipment': shipment})
