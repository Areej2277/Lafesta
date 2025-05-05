from django.urls import path
from . import views

app_name="shipping"

urlpatterns=[
    path("create_payment/<int:rental_id>/",views.create_payment,name="create_payment"),
    path("payment_response/", views.payment_response, name="payment_response"),
    path("create_shipment/<int:request_id>/",views.create_shipment,name="create_shipment"),
    path("Payment_confirmation/<int:rental_id>/",views.Payment_confirmation,name="Payment_confirmation"),
    path("order_verification/<int:adress_id>/<int:rental_id>/",views.order_verification,name="order_verification"),
    path("track_shipment/<int:rental_id>/", views.track_shipment, name="track_shipment"),
    path("manage_shipments/", views.manage_shipments, name="manage_shipments"),
    path("update_shipment_status/<int:shipment_id>/", views.update_shipment_status, name="update_shipment_status"),

]