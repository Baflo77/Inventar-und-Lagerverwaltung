from django.urls import path
from . import views

urlpatterns = [

    # HTML (Frontend)
    path("", views.deliveries_page, name="deliveries_page"),
    path("create/", views.delivery_create, name="delivery_create"),
    path("<int:id>/edit/", views.delivery_edit, name="delivery_edit"),
    path("<int:id>/delete/", views.delivery_delete, name="delivery_delete"),
    path("<int:id>/status/", views.delivery_status, name="delivery_status"),

    # API (Swagger / REST)
    path("api/", views.show_deliveries, name="api_deliveries"),
    path("api/<int:pk>/", views.show_delivery_details, name="api_delivery_detail"),
]