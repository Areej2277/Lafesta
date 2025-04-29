from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home_view, name="home"),
    path('about/', views.about_view, name="about"),
    path('contact/', views.contact_view, name="contact"),
    path('messages/', views.messages_view, name="messages"),  # admin only
    path('messages/reply/<int:message_id>/', views.reply_message_view, name="reply_message"),
    path('my_messages/', views.my_messages_view, name="my_messages"),
    path('privacy-policy/', views.privacy_policy_view, name="privacy_policy"),
]