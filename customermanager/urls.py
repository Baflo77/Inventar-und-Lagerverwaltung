"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    # HTML (Browser)

    path("", views.customers_page, name="customers_page"),
    path("create/", views.create_customer, name="customer_create"),
    path("<int:id>/edit/", views.edit_customer, name="customer_edit"),
    path("<int:id>/delete/", views.delete_customer, name="customer_delete"),

    # API (Postman / Tests)

    path("customers/", views.show_customer, name="customer_list"),
    path("customers/<int:id>/", views.show_customer_details, name="customer_detail"),
    path("customers/first/", views.show_first_customer, name="customer_first"),
    path("customers/write/", views.write_customer, name="customer_write"),
]


