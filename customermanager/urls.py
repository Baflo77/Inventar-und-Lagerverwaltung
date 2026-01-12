from django.urls import path
from . import views

urlpatterns = [

    # HTML (Browser)
    path("", views.customers_page, name="customers_page"),
    path("create/", views.create_customer, name="customer_create"),
    path("<int:id>/edit/", views.edit_customer, name="customer_edit"),
    path("<int:id>/delete/", views.delete_customer, name="customer_delete"),

    # API (Swagger / Postman)
    path("api/", views.customers_api, name="customers_api"),
    path("api/<int:id>/", views.customer_api_detail, name="customer_api_detail"),
]