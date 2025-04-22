from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home_view, name="home"),
    path('about/', views.about_view, name="about"),
    path('contact/', views.contact_view, name="contact"),
    path('messages/', views.messages_view, name="messages"),  # admin only
]