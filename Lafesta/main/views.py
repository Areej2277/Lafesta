from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import ContactMessage
from dresses.models import Dress  # ✅ Import the model from the dresses app

def home_view(request):
    new_dresses = Dress.objects.order_by('-created_at')[:6]  # ✅ Latest 6 dresses added
    return render(request, 'main/home.html', {'new_dresses': new_dresses})

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

@user_passes_test(lambda u: u.is_superuser)
def messages_view(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'main/messages.html', {"messages_list": messages_list})
# Create your views here.
