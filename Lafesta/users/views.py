from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.contrib import messages
from .models import Profile

# User Registration View
def signup_view(request: HttpRequest):
    if request.method == "POST":
        try:
            with transaction.atomic():
                new_user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password"],
                    email=request.POST["email"],
                    first_name=request.POST["first_name"],
                    last_name=request.POST["last_name"]
                )
             # Create a corresponding profile for the user
                profile = Profile(
                    user=new_user,
                    phone_number=request.POST["phone_number"],
                    user_type=request.POST["user_type"],
                    city=request.POST["city"],
                    profile_image=request.FILES.get("profile_image", Profile._meta.get_field('profile_image').get_default())
                )
                profile.save()

                messages.success(request, "Account created successfully!")
                return redirect("users:signin")

        except IntegrityError:
            messages.error(request, "Username already exists.")
        except Exception as e:
            messages.error(request, "Error during registration.")
            print(e)

    return render(request, "users/signup.html")

# User Login View
def signin_view(request: HttpRequest):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"]
        )

        if user:
            login(request, user)
            messages.success(request, "Signed in successfully!")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "users/signin.html")

# User Logout View
def logout_view(request: HttpRequest):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("users:signin")

# View for showing a user's public profile
def profile_view(request: HttpRequest, username: str):
    user = get_object_or_404(User, username=username)
    return render(request, "users/profile.html", {"user": user})

# Profile Update View for authenticated users
def update_profile_view(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be signed in to edit your profile.")
        return redirect("users:signin")

    if request.method == "POST":
        try:
            with transaction.atomic():
                user = request.user
                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.save()

                profile = user.profile
                profile.phone_number = request.POST["phone_number"]
                profile.city = request.POST["city"]
                profile.user_type = request.POST["user_type"]

                if "profile_image" in request.FILES:
                    profile.profile_image = request.FILES["profile_image"]

                profile.save()

                messages.success(request, "Profile updated successfully!")

        except Exception as e:
            messages.error(request, "Failed to update profile.")
            print(e)

    return render(request, "users/update_profile.html")

# Create your views here.
