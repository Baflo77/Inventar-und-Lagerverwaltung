from django.urls import path
from . import views

urlpatterns = [
    path("", views.deliveryitem_list, name="deliveryitem_list"),
]