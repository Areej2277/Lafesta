from django.shortcuts import render ,redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .models import Bookmark,Adress
from dresses.models import Dress
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
    #return redirect("dresses:dress_detail",dress_id=dress_id)
    return redirect("dress_detail",dress_id=dress_id)
#عشان اعرض الفساتين المفضلة 
#تحتاج تعديل الفيو و الصفحة نفسها 
def favorites_list(request:HttpRequest ,user_id):

    return render(request ,'customer/favorites_list.html')

def add_adress(request:HttpRequest):
    if request.method=="POST":
        #adress_Form = AdressForm(request.POST)
        #if adress_Form.is_valid():
            #adress_Form.instance.customer = request.user
            #adress_Form.save()
        new_adress=Adress(city=request.POST["city"], neighborhood=request.POST["neighborhood"],postcode=request.POST["postcode"],shipping_company=request.POST["shipping_company"],comments=request.POST["comments"],user=request.user)
        new_adress.save()
            #لا تنسي تغيري الري دايركت لصفحة الشحن بعد ما تسويها
        return redirect('shipping:create_payment')
        
        #else:
            #print("not falid form")
        
    return render(request ,'customer/add_adress.html')

#يحتاج تعديل الصفحة و الفيو 
def my_adress(request:HttpRequest):

    adress = Adress.objects.filter(user=request.user)

    return render(request ,'customer/my_adress.html',{"adress":adress})

def update_adress(request:HttpRequest ,adress_id:int):
    adress = Adress.objects.get(pk=adress_id, user=request.user)
    if request.method=="POST":
            new_adress=Adress(city=request.POST["city"], neighborhood=request.POST["neighborhood"],postcode=request.POST["postcode"],comments=request.POST["comments"],user=request.user)
            new_adress.save()
            #لا تنسي تغيري الري دايركت لصفحة الشحن بعد ما تسويها
            return redirect('main:home')
    
    return render(request ,'customer/update_adress.html',{"adress":adress})

def delete_adress(request:HttpRequest ,adress_id:int):
    adress = Adress.objects.get(pk=adress_id, user=request.user)
    adress.delete()
    #غيري الريدايركت خليه لصفحة الادريس
    return redirect("customer:my_adress")


