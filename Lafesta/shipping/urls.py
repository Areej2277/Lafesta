from django.urls import path
from . import views

app_name="shipping"

urlpatterns=[
    path("create_payment/<int:request_id>/",views.create_payment,name="create_payment"),
    path("create_shipment/<int:request_id>/",views.create_shipment,name="create_shipment"),
    path("Payment_confirmation/<payment_id>/",views.Payment_confirmation,name="Payment_confirmation"),
    
]