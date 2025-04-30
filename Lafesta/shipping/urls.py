from django.urls import path
from . import views

app_name="shipping"

urlpatterns=[
    path("create_payment/<int:request_id>/",views.create_payment,name="create_payment"),
    path("create_shipment/<int:request_id>/",views.create_shipment,name="create_shipment"),
    path("Payment_confirmation/<payment_id>/",views.Payment_confirmation,name="Payment_confirmation"),

    path("track_shipment/<int:rental_id>/", views.track_shipment, name="track_shipment"),

    path("manage_shipments/", views.manage_shipments, name="manage_shipments"),
    path("update_shipment_status/<int:shipment_id>/", views.update_shipment_status, name="update_shipment_status"),


]