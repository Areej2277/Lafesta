from django.shortcuts import render ,redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .models import Bookmark,Rentalrequest,Adress #احط الموديل حق البوك مارك في نفس الاب حقي و اذا كان في اب ثاني احط  اسم الاب قبل النقطة
#لا تسني تستدعي مودل الفساتين من اب ايمان 

# Create your views here.

# للمفضلة 
#اخلي اريج تضيف لي هذا السطر في البيس 
#<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">

#خلي ايمان تضيف هذي السطور عندها في الفيو الديتيلز حقت الفساتين عشان يضبط الفستان 
#is_bookmarked =Bookmark.objects.filter(user=request.user,dress=dress).exists() if request.user.is_authenticated else False
#بعيدين في الريتيرن في نفس الفيو حق الديتيلز حقت الفستان تمرر {"is_bookmarked":is_bookmarked}

#داخل التمبلت حق الديتيلز للفستان تحط لي هذي الاسطر 
#<div class="d-flex justify-content-between align-items-start">
    #<a href="{% url 'app_name:add_bookmark' dress.id%}">
    #   {% if is_bookmarked %}
    #   <i class="bi bi-heart-fill"></i>
    #   {% else %}
    #   <i class="bi bi-heart"></i>
    #   {% endif %}
    #</a>
#</div>

def add_bookmark(request:HttpRequest,dress_id):
    if not request.user.is_authenticated:
        messages.error(request, "Only registered user can add bookmarks","alert-danger")
        return redirect("acconts:sign_in")#هنا توجيه لصفحة التسجيل اللي سوتها اريج لو الاسم حقها غير , غيريه
    
    try:
        dress= Dress.objects.get(pk=dress_id)

        bookmark=Bookmark.objects.filter(user=request.user,dress=dress).first()

        if not bookmark:
            new_bookmark =Bookmark(user=request.user,dress=dress)
            new_bookmark.save()
            messages.success(request, "The dress has been added to your favorites list" , "alert-success")
        else:
            bookmark.delete
            messages.warning(request, "The dress has been removed from the favorites list" ,"alert-warning")
    except Exception as e:
        print(e)

    return redirect("صفحة تفاصيل الفستان من اب ايمان",dress_id=dress_id)
#عشان اعرض الفساتين المفضلة 
def favorites_list(request:HttpRequest ,user_id):

    return render(request ,'favorites_list.html')

def  create_rentalrequest(request:HttpRequest):
      if request.method=="POST":
        new_request=Rentalrequest(rentalDuration=request.POST["rentalDuration"],request_status=request.POST["request_status"])
        new_request.save()
        return redirect('main:home')

      return render(request ,'create_rentalrequest.html')

def add_adress(request:HttpRequest):
    if request.method=="POST":
        new_adress=Adress(City=request.POST["City"], neighborhood=request.POST["neighborhood"],postcode=request.POST["postcode"],comments=request.POST["comments"])
        new_adress.save()
        return redirect('main:home')

    return render(request ,'add_adress.html')


