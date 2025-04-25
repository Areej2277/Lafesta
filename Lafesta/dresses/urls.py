from django.urls import path
from . import views

urlpatterns = [
    path('my/', views.my_dresses, name='my_dresses'),
    path('<int:dress_id>/', views.dress_detail, name='dress_detail'),  # ✅ هذا المطلوب

    path('add/', views.add_dress, name='add_dress'),
    path('<int:dress_id>/edit/', views.edit_dress, name='edit_dress'),
    path('<int:dress_id>/delete/', views.delete_dress, name='delete_dress'),
    path('<int:dress_id>/rent/', views.rent_dress, name='rent_dress'),  # ✅ رابط صفحة الاستئجار
    path('rental/requests/', views.rental_requests, name='rental_requests'),



]
