from django.urls import path
from . import views

urlpatterns = [
    path("", views.deliveries_page, name="deliveries_page"),

    # API
    path("api/", views.show_deliveries, name="api_deliveries"),
    path("api/<int:pk>/", views.show_delivery_details, name="api_delivery_detail"),
]