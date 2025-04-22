from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import ContactMessage

def home_view(request):
    return render(request, 'main/home.html')

def about_view(request):
    return render(request, 'main/about.html')

def contact_view(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            message=request.POST["message"]
        )
        return redirect("main:contact")

    return render(request, "main/contact.html")

# يظهر فقط للأدمن
@user_passes_test(lambda u: u.is_superuser)
def messages_view(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'main/messages.html', {"messages_list": messages_list})
# Create your views here.
