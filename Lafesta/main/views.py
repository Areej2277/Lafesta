from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import ContactMessage
from dresses.models import Dress, Review  # ✅ Import the model from the dresses app


# Home page view – displays the latest added dresses
def home_view(request):
    new_dresses = Dress.objects.order_by('-created_at')[:6]  # ✅ Latest 6 dresses added
    reviews = Review.objects.select_related('user').order_by('-created_at')[:6]
    return render(request, 'main/home.html', {
        'new_dresses': new_dresses,
        'reviews': reviews,
        })

def about_view(request):
    return render(request, 'main/about.html')

# Contact page view – handles message submission and success notification
def contact_view(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            message=request.POST["message"]
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect("main:contact")
    return render(request, "main/contact.html")

# Admin-only view – shows a list of all contact messages
@user_passes_test(lambda u: u.is_superuser)
def messages_view(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'main/messages.html', {"messages_list": messages_list})

# Admin reply handler – saves admin reply to a message
def reply_message_view(request, message_id):
    if request.method == "POST":
        message = get_object_or_404(ContactMessage, id=message_id)
        reply = request.POST.get("reply")
        message.reply = reply
        message.save()
        return redirect("main:messages")
    
# Logged-in user view – shows their messages that have received admin replies   
@login_required
def my_messages_view(request):
    user_messages = ContactMessage.objects.filter(
        email=request.user.email,
        reply__isnull=False
    ).order_by('-created_at')
    return render(request, "main/my_messages.html", {"user_messages": user_messages})

# Privacy Policy page view
def privacy_policy_view(request):
    return render(request, 'main/privacy_policy.html')

# Create your views here.
