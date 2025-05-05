from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from .models import Shipment ,Payment
from dresses.models import Rental
from customer.models import Adress
from django.contrib import messages
from datetime import datetime
import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging
from dotenv import load_dotenv
import os

load_dotenv()

# طباعة قيمة السرية للتأكد من تحميلها
#secret_key = os.getenv('MOYASAR_SECRET_KEY')
#print("Moyasar Secret Key from env:", secret_key)

# Create your views here.
def create_payment(request:HttpRequest,  rental_id):
    
    rental=get_object_or_404(Rental,id=rental_id)

    try:
        address = Adress.objects.get(rental=rental)
    except Adress.DoesNotExist:
        address = None


    if request.method=="POST":
        #هنا بننشئ السجل حق الدفع المحلي 
        payment=Payment.objects.create(
            rental=rental,
            amount=rental.total_price,
            refID=random.randint(100000, 999999),
            status=data['status'],
            moyasar_id=data['id']
        )
        #هنا يجهز البيانات اللي اخذها من سجل الدفع المحلي عشان يرسلها لمنصة ميسر 
        headers= {
            "Authorization": f"Bearer {os.getenv('MOYASAR_SECRET_KEY')}",
            "Content-Type":"application/json" 
        }
        data={
            "amount":int(rental.total_price * 100),
            "currency": "SAR",
            "description": f"Rental payment for rental ID {rental.id}",
            "callback_url": request.build_absolute_uri('/payment_response/'),
            "redirect_url": request.build_absolute_uri(reverse('shipping:Payment_confirmation', args=[payment.id, rental.id])),
            "source": {
            "type": "creditcard",
            "name": request.POST.get("name"),
            "number": request.POST.get("card_number"), 
            "cvc": request.POST.get("cvc"),            
            "month": request.POST.get("expiry_month"), 
            "year": request.POST.get("expiry_year")

    }
        } 
        try:
            
            response=requests.post("https://api.moyasar.com/v1/payments", json=data,headers=headers )

            if response.status_code == 200:
                result=response.json()
                payment.moyasar_id = result["id"]
                source = result.get("source",{})
                payment.invoice_url = source.get ("checkout_url", "")
                payment.status = result["status"]
                payment.save()
                #عشان تتحدث حالة الطلب في صفحة تتبع الطلب 
                #rental.status = 'confirmed'
                #rental.save()
                #هنا بدل ما تنفتح الصفحة اللي سويتها للدفع تنفتح صفحة الدفع حقت ميسر عشان كذا حذفت البوست اللي قبل لاني ما احتاج احفظ بينات الدفع للعميل نفس ما قال الاستاذ
                return redirect(result["source"]["checkout_url"])
                
            else:
                messages.error(request,"Payment failed,Try again ")
                return redirect("dresses:my_orders")
        except Exception as e:
            messages.error(request, f"Error while initiating payment: {str(e)}")
            return redirect("dresses:my_orders", rental_id=rental.id)    

        #messages.success(request, "Payment was created successfully!")
        # لو فيه حقل rental: rental=rental_request
        #return redirect('shipping:Payment_confirmation', payment_id=new_payment.id, rental_id=rental.id)
    #else:
        #messages.error(request, "Payment creation failed")
        
    return render(request ,'shipping/new_payment.html' ,{'rental': rental, 'address': address ,'amount': int(rental.total_price * 100)})


# def create_shipment(request:HttpRequest ,request_id):
#     rental_request=Rental.objects.get(pk=request_id)
#     adress = Adress.objects.filter(user=rental_request.customer).first()

#     if request.method=="POST":from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_response(request: HttpRequest):
    if request.method == "POST":
        try:
            import json
            data =json.loads(request.body)
            moyasar_id = data.get("id")
            status = data.get("status")
            if not moyasar_id: 
                return JsonResponse({"error":"Missing pament id"}, status=400)
            payment = Payment.objects.get(moyasar_id = moyasar_id)
            payment.status = status
            payment.save()
             #الشرط اللي تحتاجه صفحة الطلبات لتاكيد الدفع 
            if status == "paid":
                payment.rental.status = 'confirmed'
                payment.rental.save()
            return JsonResponse({"message": "Callback processed."}, status=200)

        except Exception as e:
            return JsonResponse({"error":str(e)}, status=400)
    else:
        return JsonResponse({"message": "Invalid method."}, status=405)

    
def order_verification(request:HttpRequest, adress_id ,rental_id):
    
    adress = get_object_or_404(Adress, id=adress_id)
    rental= get_object_or_404(Rental, id=rental_id)
    if request.method == "POST":
        return redirect('shipping:create_payment',rental_id=rental.id,)

    return render(request ,'shipping/order_verification.html',{'adress':adress ,'rental': rental})


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
            owner_name=request.POST["owner_name"],
            owner_phone=request.POST["owner_phone"],
            Pick_up_address=request.POST["Pick_up_address"],
            expected_Pick_up_date=request.POST["expected_Pick_up_date"],
            shipping_company=request.POST["shipping_company"],
            expected_delivery_date=request.POST["expected_delivery_date"],
            comments=request.POST["comments"],
            rental=rental_request,       
            adress=adress
        )
        new_Shipment.save()

        # ✅ بعد الإنشاء يروح لصفحة إدارة الشحنات
        return redirect('shipping:manage_shipments')

    return render(request, 'shipping/new_shipment.html', {'rental': rental_request})




def Payment_confirmation(request:HttpRequest,rental_id):
    moyasar_id = request.GET.get('id')
    print("🔑 Moyasar Secret Key from env:", os.getenv('MOYASAR_SECRET_KEY'))
    rental= get_object_or_404(Rental, id=rental_id)
    payment = None
    print("🔍 Moyasar ID from request:", moyasar_id)
    #status = payment.status if payment else 'failed'
    #payment = None # get_object_or_404(Payment, id=payment_id)
    if not moyasar_id:
        messages.error(request, "There is no payment ID in the link ")
        return render(request,'shipping/Payment_confirmation.html',{'rental':rental,'payment':None, 'status':'failed',' message':'Payment failure'})
    response= requests.get(f"https://api.moyasar.com/v1/payments/{moyasar_id}",auth=(os.getenv('MOYASAR_SECRET_KEY'), ''))
    print("📡 Moyasar API status code:", response.status_code)
    print("📡 Moyasar API response text:", response.text)

    if response.status_code == 200: 
        result = response.json()
        status =result.get("status").lower()
        logging.debug(f"Payment status from Moyasar API: {status}")
        print("🔍 Full Moyasar response:", result)
        for p in Payment.objects.all():
            print("💾 Stored Moyasar ID in DB:", p.moyasar_id)

        try:
            payment = Payment.objects.get(moyasar_id=moyasar_id)
            payment.status = status
            payment.save()
        except Payment.DoesNotExist:
            ref_id=result.get('source', {}).get('reference_number')
            
            if ref_id and ref_id.isdigit():
                ref_id = int(ref_id)
            else:
                ref_id = random.randint(100000, 999999)
            amount = result.get('amount', 0)
            payment = Payment(moyasar_id=moyasar_id, status=status,refID=ref_id,amount=amount,rental=rental) 
            payment.save()
        
        if status == "paid":
            rental.status = 'confirmed'
            rental.save()
            return render(request, 'shipping/Payment_confirmation.html',{'rental':rental,'payment':payment,'status': 'success','message':'Payment Successfully Completed'})
        else:
            rental.status = 'failed'
            logging.debug("Payment failed or message not approved.")
            return render(request,'shipping/Payment_confirmation.html',{'rental':rental,'payment':payment,'status':'failed','message':'Payment failed'})
    else:
        print("📡 Moyasar API status code:", response.status_code)
        print("📡 Moyasar API response text:", response.text)
        return render(request,'shipping/Payment_confirmation.html',{'rental':rental,'payment':payment,'status':'error','message':'Payment platform connection error'})

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
    shipments = Shipment.objects.filter(rental__dress__owner=user).order_by('-created_at')

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
