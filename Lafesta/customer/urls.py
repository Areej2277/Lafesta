from django.urls import path
from . import views

app_name="customer"

urlpatterns=[
    path("bookmarks/add/<dress_id>/",views.add_bookmark,name="add_bookmark"),
    path("favorites_list/<user_id>/",views.favorites_list,name="favorites_list"),
    path("add_adress/<int:rental_id>/",views.add_adress,name="add_adress"),
    path("my_adress/",views.my_adress,name="my_adress"),
    path("update_adress/<int:adress_id>/",views.update_adress,name="update_adress"),
    path("delete_adress/<int:adress_id>/",views.delete_adress,name="delete_adress"),
]