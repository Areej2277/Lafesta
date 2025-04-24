from django.urls import path
from . import views

app_name="user"

urlpatterns=[
    path("bookmarks/add/<dress_id>/",views.add_bookmark,name="add_bookmark"),
    path("favorites_list/<user_id>/",views.favorites_list,name="favorites_list"),
    path("newrentalrequest/",views.create_rentalrequest, name="create_rentalrequest")
]