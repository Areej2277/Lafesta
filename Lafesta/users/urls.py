from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("signin/", views.signin_view, name="signin"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/<str:username>/", views.profile_view, name="profile"),
    path("profile/edit/", views.update_profile_view, name="edit_profile"),
]
