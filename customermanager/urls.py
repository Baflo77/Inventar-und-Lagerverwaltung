from django.urls import path
from . import views

urlpatterns = [

    # HTML (Browser)
    path("", views.customers_page, name="customers_page"),
    path("create/", views.create_customer, name="customer_create"),
    path("<int:id>/edit/", views.edit_customer, name="customer_edit"),
    path("<int:id>/delete/", views.delete_customer, name="customer_delete"),

    # API (Swagger / Postman)
    path("customers/", views.show_customer, name="customer_list"),
    path("customers/first/", views.show_first_customer, name="customer_first"),
    path("customers/write/", views.write_customer, name="customer_write"),
    path("customers/<int:id>/", views.show_customer_details, name="customer_detail"),
]