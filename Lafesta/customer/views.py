from django.shortcuts import render ,redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .models import Bookmark,Adress
from dresses.models import Dress,Rental
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

#from .forms import AdressForm
#from django.contrib.auth.decorators import login_required
# Create your views here.

#خلي ايمان تضيف هذي السطور عندها في الفيو الديتيلز حقت الفساتين عشان يضبط الفستان 
#is_bookmarked =Bookmark.objects.filter(user=request.user,dress=dress).exists() if request.user.is_authenticated else False
#بعيدين في الريتيرن في نفس الفيو حق الديتيلز حقت الفستان تمرر {"is_bookmarked":is_bookmarked}


def add_bookmark(request:HttpRequest,dress_id):
    if not request.user.is_authenticated:
        messages.error(request, "Only registered user can add bookmarks","alert-danger")
        return redirect("users:signin")
    try:
        dress= Dress.objects.get(pk=dress_id)

        bookmark=Bookmark.objects.filter(user=request.user,dress=dress).first()

        if not bookmark:
            new_bookmark =Bookmark(user=request.user,dress=dress)
            new_bookmark.save()
            messages.success(request, "The dress has been added to your favorites list" , "alert-success")
        else:
            bookmark.delete()
            messages.warning(request, "The dress has been removed from the favorites list" ,"alert-warning")
    except Exception as e:
        print(e)
    return redirect("dresses:dress_detail",dress_id=dress_id)
#عشان اعرض الفساتين المفضلة 
#تحتاج تعديل الفيو و الصفحة نفسها 
def favorites_list(request:HttpRequest ,user_id):

    return render(request ,'customer/favorites_list.html')

def add_adress(request:HttpRequest ,rental_id):
    rental = Rental.objects.get(id=rental_id)
    if request.method=="POST":
        #adress_Form = AdressForm(request.POST)
        #if adress_Form.is_valid():
            #adress_Form.instance.customer = request.user
            #adress_Form.save()
        new_adress=Adress(city=request.POST["city"], neighborhood=request.POST["neighborhood"],postcode=request.POST["postcode"],shipping_company=request.POST["shipping_company"],comments=request.POST["comments"],user=request.user,rental=rental)
        new_adress.save()
        messages.success(request, "Address added successfully!")
        return redirect('shipping:order_verification',rental_id=rental.id,adress_id=new_adress.id)
    else:
        messages.warning(request, "Please fill in all required fields.")
        #else:
            #print("not falid form")
        
    return render(request ,'customer/add_adress.html',{'rental': rental})

def adress_choice (request:HttpRequest ,rental_id):
    rental=get_object_or_404(Rental,id=rental_id)
    try:
        adress = Adress.objects.get(user=request.user)
    except Adress.DoesNotExist:
        return redirect("customer:add_adress",rental_id=rental_id)
    
    if request.method =="POST":
        if "use_existing_address" in request.POST:
            adress.rental=rental
            adress.save()
            return redirect('shipping:order_verification',rental_id=rental.id,adress_id=adress.id)
        elif "update_address" in request.POST:
            return redirect("customer:update_adress",adress_id=adress.id)


    return render(request ,'customer/adress_choice.html', {'rental': rental ,'adress':adress})


#يحتاج تعديل الصفحة و الفيو 
def my_adress(request:HttpRequest):

    adress = Adress.objects.filter(user=request.user)

    return render(request ,'customer/my_adress.html',{"adress":adress})

def update_adress(request:HttpRequest ,adress_id:int):
    try:
        rental = Rental.objects.filter(customer=request.user).latest('id')

    except ObjectDoesNotExist:
        
        messages.warning(request,"You don't have any rent requests yet." )
        return redirect("dresses:my_dresses")
    
    adress= get_object_or_404(Adress,pk=adress_id, user=request.user)
    
    if request.method=="POST":
        adress.city=request.POST["city"]
        adress.neighborhood=request.POST["neighborhood"]
        adress.postcode=request.POST["postcode"]
        adress.comments=request.POST["comments"]
        adress.rental=rental
        adress.save()
        messages.success(request, "Address updated successfully!")
            #لا تنسي تغيري الري دايركت لصفحة الشحن بعد ما تسويها
        return redirect('shipping:order_verification',rental_id=rental.id,adress_id=adress.id)
    
    return render(request ,'customer/update_adress.html',{"adress":adress,'rental': rental})

def delete_adress(request:HttpRequest ,adress_id:int):
    adress = Adress.objects.get(pk=adress_id, user=request.user)
    adress.delete()
    #غيري الريدايركت خليه لصفحة الادريس
    return redirect("customer:my_adress")

